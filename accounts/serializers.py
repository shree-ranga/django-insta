from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import TestImageUpload

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    # need id field to update following in UserDetailSerializer
    id = serializers.IntegerField(required=False)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "full_name", "profile_image_url", "bio")

    def get_full_name(self, obj):
        return str(obj.first_name + " " + obj.last_name)


class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    total_followers = serializers.SerializerMethodField()
    total_following = serializers.SerializerMethodField()
    followers = UserListSerializer(many=True)
    following = UserListSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "full_name",
            "profile_image_url",
            "bio",
            "followers",
            "following",
            "total_followers",
            "total_following",
        )

    def get_full_name(self, obj):
        return str(obj.first_name + " " + obj.last_name)

    def get_total_followers(self, obj):
        return obj.followers.count()

    def get_total_following(self, obj):
        return obj.following.count()

    def update(self, instance, validated_data):
        following_user = validated_data.pop("following")
        user = following_user[0]
        if "id" in user.keys():
            instance_following_user = User.objects.get(id=user["id"])
            instance.following.add(instance_following_user)
            instance.save()
        return instance


class TestImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestImageUpload
        fields = "__all__"
