from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .serializers import UserListSerializer, UserDetailSerializer, FollowSerializer
from .models import Follow

User = get_user_model()


class UserListAPIView(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except:
            return Response(
                {"error": "User object not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, pk=None):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowUnfollowAPIView(APIView):
    def post(self, request):
        serializer = FollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        print(request.data)
        data = request.data
        follower_user_id = request.user.id
        following_user_id = data.get("following_user_id", None)
        if following_user_id is not None:
            instance = Follow.objects.get(
                follower_user_id=follower_user_id, following_user_id=following_user_id
            )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Following user Does not exit"}, status=status.HTTP_404_NOT_FOUND
        )


class UserFollowingListAPIView(APIView):
    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except:
            raise ValidationError("User does not exit")

    def get_queryset(self, pk):
        user = self.get_object(pk=pk)
        following_users = user.following.all()
        return following_users

    def get(self, request, pk=None):
        queryset = self.get_queryset(pk)
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFollowersListAPIView(APIView):
    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except:
            raise ValidationError("User does not exit")

    def get_queryset(self, pk):
        user = self.get_object(pk=pk)
        following_users = user.followers.all()
        return following_users

    def get(self, request, pk=None):
        queryset = self.get_queryset(pk)
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

