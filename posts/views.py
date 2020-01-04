from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, JSONParser

from .serializers import PostSerializer, LikeSerializer
from .models import Post, Like


class PostCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, JSONParser)

    def post(self, request):
        self.create(request)
        return Response(
            {"msg": "Post upload successful..."}, status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostListView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id", None)
        if user_id is not None:
            queryset = Post.objects.filter(owner=user_id)
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserFeedView(APIView):
    # TODO: - Update cache after post
    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        following_list = []
        user_id = request.user.id
        following_list.append(user_id)
        user_following_ids = list(
            request.user.following.all().values_list("id", flat=True)
        )
        following_list += user_following_ids
        queryset = Post.objects.filter(owner__in=following_list)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeCreateView(APIView):
    def post(self, request):
        post_id = request.data["post_id"]
        user_id = request.user.id
        data = {"post": post_id, "user": user_id}
        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "like_created succesfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnlikeView(APIView):
    def delete(self, request):
        post_id = request.data["post_id"]
        user_id = request.user.id
        l_instance = Like.objects.get(post=post_id, user=user_id)
        p_instance = Post.objects.get(id=post_id)
        p_instance.likes_count = F("likes_count") - 1
        p_instance.save()
        l_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckLikeView(APIView):
    def post(self, request):
        post_id = request.data["post_id"]
        user_id = request.user.id
        if Like.objects.filter(post=post_id, user=user_id).exists():
            return Response({"liked": True}, status=status.HTTP_200_OK)
        return Response({"liked": False}, status=status.HTTP_200_OK)
