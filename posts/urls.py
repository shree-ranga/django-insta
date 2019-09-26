from django.urls import path

from .views import PostCreateView, PostListView, UserFeedView

urlpatterns = [
    path("upload/", PostCreateView.as_view(), name="upload_post"),
    path("user/", PostListView.as_view(), name="user_posts"),
    path("feed/", UserFeedView.as_view(), name="feed"),
]
