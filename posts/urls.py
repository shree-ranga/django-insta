from django.urls import path

from .views import PostCreateView

urlpatterns = [path("upload/", PostCreateView.as_view(), name="upload_post")]
