from rest_framework import serializers

from .models import *


class TaggedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaggedItem
        fields = "__all__"
