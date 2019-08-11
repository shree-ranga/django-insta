from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError

# from PIL import Image

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    TestImageUploadSerializer,
)
from .models import TestImageUpload

User = get_user_model()


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.data.get("token", None)
        if token:
            token = Token.objects.filter(key=token)[0]
            token.delete()
        else:
            return Response(
                {"message": "Token not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


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
