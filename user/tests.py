import faker
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from common.tests import BaseTestCase

from .models import User


class UserRegisterationAPITestCase(BaseTestCase):
    def test_user_register_api_should_success(self):
        client = APIClient()
        user_data = {
            "email": faker.Faker().email(),
            "password": "password",
            "nickname": faker.Faker().name(),
            "lives_in": faker.Faker().city(),
            "birthday": faker.Faker().date_of_birth().isoformat(),
            "bio": "Hello World!",
        }
        response = client.post(reverse("user:register"), user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_exists = User.objects.filter(email=user_data["email"]).exists()
        self.assertTrue(user_exists)

    def test_user_register_api_should_fail(self):
        client = APIClient()
        user_data = {
            "email": faker.Faker().email(),
            "password": "password",
            "nickname": faker.Faker().name(),
            "lives_in": faker.Faker().city(),
            "birthday": faker.Faker().date_of_birth().isoformat(),
            "bio": "Hello World!",
        }

        # call the endpoint twice with the same email
        client.post(reverse("user:register"), user_data, format="json")

        response = client.post(reverse("user:register"), user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = response.json()

        self.assertEqual(len(response["email"]), 1)
        self.assertEqual(
            response["email"][0], "user with this email address already exists."
        )

    def test_user_register_api_should_fail_with_invalid_data(self):
        client = APIClient()
        user_data = {
            "email": "invalid-email",
            "password": "password",
            "nickname": faker.Faker().name(),
            "lives_in": faker.Faker().city(),
            "birthday": faker.Faker().date_of_birth().isoformat(),
            "bio": "Hello World!",
        }
        response = client.post(reverse("user:register"), user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = response.json()

        self.assertEqual(len(response["email"]), 1)
        self.assertEqual(response["email"][0], "Enter a valid email address.")


class UserLoginAPITestCase(BaseTestCase):

    def test_login_api_should_success(self):
        client = APIClient()
        user = self._create_test_user()
        user_data = {"email": user.email, "password": "password"}
        response = client.post(reverse("user:login"), user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_login_api_should_fail_invalid_credentials(self):
        client = APIClient()
        user = self._create_test_user()
        user_data = {"email": user.email, "password": "invalid-password"}
        response = client.post(reverse("user:login"), user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAuthRefreshTokenAPITestCase(BaseTestCase):

    def test_token_refresh_api_should_success(self):
        client = APIClient()
        user = self._create_test_user()
        user_data = {"email": user.email, "password": "password"}
        # get valid refresh token
        response = client.post(reverse("user:login"), user_data, format="json")
        refresh_token = response.json()["refresh"]
        # refresh token
        response = client.post(
            reverse("user:refresh-token"),
            {"refresh": refresh_token},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_token_refresh_api_should_fail(self):
        client = APIClient()
        response = client.post(
            reverse("user:refresh-token"), {"refresh": "invalid-token"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserUpdateAPITestCase(BaseTestCase):

    def test_user_update_api_should_success(self):
        client = APIClient()
        user = self._create_test_user()
        user_data = {
            "email": user.email,
            "password": "password",
            "nickname": faker.Faker().name(),
            "lives_in": faker.Faker().city(),
            "birthday": faker.Faker().date_of_birth().isoformat(),
            "bio": "Hello World!",
        }
        client.force_authenticate(user=user)
        response = client.put(
            reverse("user:update", args=[user.id]), user_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.nickname, user_data["nickname"])
        self.assertEqual(user.lives_in, user_data["lives_in"])
        self.assertEqual(user.birthday.isoformat(), user_data["birthday"])
        self.assertEqual(user.bio, user_data["bio"])

    def test_user_update_api_should_fail_with_invalid_data(self):
        client = APIClient()
        user = self._create_test_user()
        user_data = {"email": "invalid-email"}
        client.force_authenticate(user=user)
        response = client.put(
            reverse("user:update", args=[user.id]), user_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = response.json()
        self.assertEqual(len(response["email"]), 1)
        self.assertEqual(response["email"][0], "Enter a valid email address.")


class UserDeleteAPITestCase(BaseTestCase):

    def test_user_delete_api_should_success(self):
        client = APIClient()
        user = self._create_test_user()
        client.force_authenticate(user=user)
        response = client.delete(reverse("user:delete"), args=[user.id])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user_exists = User.objects.filter(id=user.id).exists()
        self.assertFalse(user_exists)

    def test_user_delete_api_should_fail(self):
        client = APIClient()
        user = self._create_test_user()
        client.force_authenticate(user=user)
        response = client.delete(reverse("user:delete", args=[user.id + 1]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        user_exists = User.objects.filter(id=user.id).exists()
        self.assertTrue(user_exists)
