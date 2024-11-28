from typing import Any

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import Token


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> None | tuple[Any, Token]:
        raw_token = request.COOKIES.get("access")
        if raw_token is None:
            return None

        try:
            validated_token: Token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError) as e:
            raise AuthenticationFailed("Invalid token.") from e

        return self.get_user(validated_token), validated_token
