from rest_framework import generics
from rest_framework import mixins
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
