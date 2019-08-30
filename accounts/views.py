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
            raise ValidationError("User does not exist")

    def get(self, request, pk=None):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentUserDetailAPIVIew(UserDetailAPIView):
    def get_object(self, pk=None):
        user = self.request.user
        return user


class FollowUnfollowAPIView(APIView):

    # follow
    # change this to get or create and get rid of check
    def post(self, request):
        data = request.data
        follower_user_id = request.user.id
        following_user_id = data.get("following_user_id")
        follow_data = {
            "follower_user": follower_user_id,
            "following_user": following_user_id,
        }
        serializer = FollowSerializer(data=follow_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # unfollow
    def delete(self, request):
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


class CheckFollow(APIView):
    # check if following and return bool response
    # may be do filtering
    def post(self, request):
        data = request.data
        follower_user_id = request.user.id
        following_user_id = data.get("following_user_id")
        if Follow.objects.filter(
            follower_user_id=follower_user_id, following_user_id=following_user_id
        ).exists():
            return Response({"following": True}, status=status.HTTP_200_OK)
        return Response({"following": False}, status=status.HTTP_200_OK)


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

