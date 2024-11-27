from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import ProductViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"transactions", TransactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
# urlpatterns = router.urls
