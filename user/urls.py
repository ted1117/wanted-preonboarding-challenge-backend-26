from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import UserViewset

router = DefaultRouter()
router.register(r"", UserViewset, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
