from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)
    password2 = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ["email", "nickname", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords must match.")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            nickname=validated_data["nickname"],
        )

        update_last_login(None, user)

        return user


class UserSchema(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "nickname",
            "is_active",
            "is_staff",
        ]
        read_only_fields = ["nickname", "email", "is_superuser", "last_login"]
