from rest_framework import serializers

from .models import Notification

from accounts.models import Follow
from accounts.serializers import UserListSerializer, FollowSerializer
from posts.models import Like
from posts.serializers import LikeSerializer, PostSerializer


class NotifiedObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Follow):
            serializer = FollowSerializer(value)
        elif isinstance(value, Like):
            serializer = LikeSerializer(value)
        else:
            raise Exception("Unexpected content type object")
        return serializer.data

    def to_internal_value(self, data):
        return super().to_internal_value(data)


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserListSerializer(required=False)
    receiver = UserListSerializer(required=False)
    content_object = NotifiedObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "sender", "receiver", "content_object", "notification_type"]
        read_only_fields = [
            "id",
        ]

