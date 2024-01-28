from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import ApplicationUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationUser
        exclude = []

    def create(self, validated_data):
        user = ApplicationUser.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationUser
        fields = (
            "uuid",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "role",
        )
        read_only_fields = ("uuid", "username", "email", "is_active")


class AuthorizeUserSerializer(BaseUserSerializer):
    pass


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)


class UserAuthSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
