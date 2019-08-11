from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError

from .serializers import *

User = get_user_model()

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
