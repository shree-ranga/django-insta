from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import TestImageUpload

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    # need id field to update following field in UserDetailSerializer?
    id = serializers.IntegerField(required=False)
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
            "followers",
        )

    def get_full_name(self, obj):
        return str(obj.first_name + " " + obj.last_name)

    def get_total_followers(self, obj):
        return obj.followers.count()

    def get_total_following(self, obj):
        return obj.following.count()


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
            "following",
            "total_followers",
            "total_following",
            "followers",
        )
        extra_kwargs = {"following": {"write_only": True}}

    def get_total_followers(self, obj):
        return obj.followers.count()

    def get_total_following(self, obj):
        return obj.following.count()

    def get_full_name(self, obj):
        return str(obj.first_name + " " + obj.last_name)

    # TODO: - Add Validation and unfollow feature
    def update(self, instance, validated_data):
        follow_user = validated_data.pop("following")
        for user in follow_user:
            if user not in instance.following.all():
                if instance.id != user.id:
                    instance.following.add(user)
                    instance.save()
                else:
                    raise ValidationError("User object cannot follow itself")
            else:
                instance.following.remove(user)
                instance.save()

        return instance


class TestImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestImageUpload
        fields = "__all__"
