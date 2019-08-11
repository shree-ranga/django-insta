from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # full_name = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            # "full_name",
            "email",
            "profile_image_url",
            "password",
        )

    def validate(self, data):
        # full_name = data.get("full_name", None)
        # data["full_name"] = full_name
        data["first_name"], data["last_name"] = self.get_first_last_name()
        return data

    def get_first_last_name(self):
        full_name = self.initial_data["full_name"]
        split_full_name = full_name.rsplit(None, 1)
        first_name = split_full_name[0]
        last_name = split_full_name[1]
        return (first_name, last_name)

    def create(self, validated_data):
        # validated_data.pop("full_name") ??
        # first_name, last_name = self.get_first_last_name()
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", None)
        email = data.get("email", None)
        password = data.get("password", None)

        if (username or email) and password:
            if username:
                user = authenticate(username=username, password=password)
            if email:
                user = authenticate(
                    username=User.objects.filter(email=email)[0], password=password
                )
            if user is not None:
                data["user"] = user
            else:
                msg = "Unable to login with given credentials. Check username, email or password"
                raise ValidationError(msg)
        else:
            msg = "Please provide username or email and password"
            raise ValidationError(msg)
        return data

    # def get_user_by_email(self):
    #     if self.email:
    #         user = User.objects.filter(email=email)
    #     return user


class LogoutSerializer(serializers.ModelSerializer):
    pass
