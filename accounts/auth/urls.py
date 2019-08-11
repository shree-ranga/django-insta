from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    # path("auth/register/upload/", UploadProfileImageView.as_view(), name="upload_profile_image"),
    path("register/api-auth-token/", obtain_auth_token, name="api_auth_token"),
]