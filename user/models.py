from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, nickname):
        if not email:
            raise ValueError("must have user email")
        user = self.model(
            email=self.normalize_email(email=email),
            nickname=nickname or email.split("@")[0],
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, nickname):
        user = self.create_user(email=email, password=password, nickname=nickname)
        user.is_superuser = True
        user.is_staff = True
        user.save(self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    nickname = models.CharField(unique=True, max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    def __str__(self) -> object:
        return self.nickname
