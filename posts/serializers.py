from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault


from .models import Post


class PostSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(
    #     read_only=True, default=CurrentUserDefault()
    # )

    class Meta:
        model = Post
        fields = ("id", "post_image", "caption", "owner")
        read_only_fields = ("id", "owner")
