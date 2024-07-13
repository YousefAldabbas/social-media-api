from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from user import views


app_name = "user"

urlpatterns = [
    path("", views.UserListView.as_view(), name="user-list"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="details"),
    path("register/", views.UserCreateView.as_view(), name="register"),
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="delete"),
    path("follow/<int:pk>/", views.UserFollow.as_view(), name="follow"),
    path("auth/login/", jwt_views.TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", jwt_views.TokenRefreshView.as_view(), name="refresh-token"),
    path("auth/verify/", jwt_views.TokenVerifyView.as_view(), name="verify-token"),
    path("me/", views.ManageUserView.as_view(), name="profile"),
]
