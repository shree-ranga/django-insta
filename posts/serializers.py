from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Post

User = get_user_model()


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "profile_image_url")


class PostSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(
        default=CurrentUserDefault(), read_only=True, required=False
    )

    class Meta:
        model = Post
        fields = ("id", "post_image", "caption", "owner", "created_at")
        read_only_fields = ("id",)

