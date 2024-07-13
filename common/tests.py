import faker

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseTestCase(TestCase):
    def _create_test_user(self) -> User: # type: ignore
        user = User.objects.create(
            email=faker.Faker().email(),
            nickname=faker.Faker().name(),
            lives_in=faker.Faker().city(),
            birthday=faker.Faker().date_of_birth().isoformat(),
            bio="Hello World!",
        )
        user.set_password("password")
        user.save()
        return user
