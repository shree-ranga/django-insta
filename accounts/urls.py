from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import *

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("users/me/", UserDetailAPIView.as_view(), name="user_detail"),
    path(
        "users/<int:pk>/following/",
        UserFollowingAPIView.as_view(),
        name="user_following_list",
    ),
    path(
        "users/<int:pk>/followers/",
        UserFollowersAPIView.as_view(),
        name="user_followers_list",
    ),
]
