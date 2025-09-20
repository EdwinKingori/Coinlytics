# Custom serializer from djoser
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseCreateSerializer
from rest_framework import serializers
from .models import CustomUser


class UserCreateSerializer(BaseCreateSerializer):
    class Meta(BaseCreateSerializer.Meta):
        model = CustomUser
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']

        def validate_username(self, value):
            if CustomUser.objects.filter(username=value).exists():
                raise serializers.ValidationError("Username already exists!")
            if len(value) < 4:
                raise serializers.ValidationError(
                    "Username must be at least 4 characters long!")
            return value

        def validate_password(self, value):
            has_uppercase = any(char.isupper() for char in value)
            has_number = any(char.isdigit() for char in value)
            has_special = any(
                char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in value)

            if not has_uppercase:
                raise serializers.ValidationError(
                    "Password must contain at least one uppercase letter.")
            if not has_number:
                raise serializers.ValidationError(
                    "password must contain at least one number.")
            if len(value) < 8:
                raise serializers.ValidationError(
                    "Password must be at least 8 characters long.")
            if not has_special:
                raise serializers.ValidationError(
                    "Password must have at least one special letter!")
            return value


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
