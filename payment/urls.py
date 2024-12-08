from django.urls import path, include
from ninja import NinjaAPI

from payment.views import api


urlpatterns = [
    path("payments/", api.urls),
]
