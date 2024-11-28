from django.shortcuts import render
from django.contrib.auth import authenticate, logout
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken


from user.models import User
from user.serializers import UserSchema, UserSerializer


# Create your views here.
class UserViewSet(ModelViewSet):
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
            refresh_token = RefreshToken.for_user(user)
            refresh = str(refresh_token)
            access = str(refresh_token.access_token)
            response = Response(
                {
                    "refresh": refresh,
                    "access": access,
                },
                status=status.HTTP_200_OK,
            )
            response.set_cookie(
                key="access",
                value=access,
                httponly=True,
                secure=True,
                samesite="Lax",
            )
            response.set_cookie(
                key="refresh",
                value=refresh,
                httponly=True,
                secure=True,
                samesite="Lax",
            )

            return response
        return Response(
            {"message": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=["post"], detail=False)
    def logout(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Refresh Token not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except InvalidToken as e:
            return Response(
                {"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )
        except AttributeError as e:
            return Response(
                {"error": "Blacklist feature not enabled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response
