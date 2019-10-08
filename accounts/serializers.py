from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Follow

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "full_name", "profile_image_url")
        read_only_fields = ("id",)

    def get_full_name(self, obj):
        return str(obj.first_name + " " + obj.last_name)


class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    total_followers = serializers.SerializerMethodField()
    total_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "full_name",
            "profile_image_url",
            "bio",
            "total_followers",
            "total_following",
        )
        read_only_fields = ("id",)

    def get_total_followers(self, obj):
        return obj.followers.count()

    def get_total_following(self, obj):
        return obj.following.count()

    def get_full_name(self, obj):
        return str(obj.first_name + " " + obj.last_name)


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", "following_user", "follower_user")
