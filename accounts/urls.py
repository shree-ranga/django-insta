from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import *

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("users/me/", UserDetailAPIView.as_view(), name="user_detail"),
    path("dummy/", DummyAPIView.as_view(), name="dummy"),  # dummy path
]
