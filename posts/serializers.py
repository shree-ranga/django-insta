from django.contrib.auth import get_user_model
from django.db.models import F

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Post, Like

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
        fields = ("id", "post_image", "caption", "owner", "likes_count", "created_at")
        read_only_fields = ("id",)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "post", "user")
        # read_only_fields = ("id", "user")

    def create(self, validated_data):
        post = validated_data.pop("post", None)
        if post:
            p = Post.objects.get(id=post.id)
            p.likes_count = F("likes_count") + 1
            p.save()
            instance = Like.objects.create(post=p, **validated_data)
        return instance

