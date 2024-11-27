from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from user.models import User
from user.serializers import UserSchema, UserSerializer


# Create your views here.
class UserViewset(ModelViewSet):
    serializer_class = UserSchema
    queryset = User.objects.all()
    serializer_classes = {
        "list": UserSchema,
        "retrieve": UserSchema,
        "create": UserSerializer,
        "delete": UserSerializer,
        "update": UserSerializer,
        "partial_update": UserSerializer,
    }

    def get_permissions(self):
        if self.action in ["create", "login"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes)

    @action(methods=["post"], detail=False)
    def login(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(
            {"message": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=["post"], detail=False)
    def logout(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
