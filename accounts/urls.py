from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import *

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user_detail"),
    path(
        "users/current/", CurrentUserDetailAPIVIew.as_view(), name="current_user_detail"
    ),
    path(
        "users/follow-unfollow/",
        FollowUnfollowAPIView.as_view(),
        name="user_follow_unfollow",
    ),
    path(
        "users/<int:pk>/followers/",
        UserFollowersListAPIView.as_view(),
        name="user_followers",
    ),
    path(
        "users/<int:pk>/following/",
        UserFollowingListAPIView.as_view(),
        name="user_following",
    ),
    path("users/check-follow/", CheckFollow.as_view(), name="check_follow"),
]
