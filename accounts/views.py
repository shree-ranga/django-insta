from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .serializers import UserListSerializer, UserDetailSerializer, UserFollowSerializer

User = get_user_model()


class UserListAPIView(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        print("PATCH", request.data)
        serializer = UserDetailSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserFollowingAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

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


class UserFollowersAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

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

    # def patch(self, request):
    #     serializer = UserFollowSerializer(request.user, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class UserFollowersAPI(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticatedOrReadOnly,)


# class UploadProfileImageView(APIView):
#     # permission_classes = (AllowAny,)
#     parser_class = (FileUploadParser,)

#     def post(self, request):
#         print(request.data)
#         serializer = TestImageUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
