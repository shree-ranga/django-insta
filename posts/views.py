from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, JSONParser

from .serializers import PostSerializer
from .models import Post


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
