from django.urls import path

from .views import (
    PostCreateView,
    PostListView,
    UserFeedView,
    LikeCreateView,
    UnlikeView,
    CheckLikeView,
)

urlpatterns = [
    path("upload/", PostCreateView.as_view(), name="upload_post"),
    path("user/", PostListView.as_view(), name="user_posts"),
    path("feed/", UserFeedView.as_view(), name="feed"),
    path("like/", LikeCreateView.as_view(), name="like_post"),
    path("unlike/", UnlikeView.as_view(), name="unlike_post"),
    path("check-like/", CheckLikeView.as_view(), name="check_like"),
]
