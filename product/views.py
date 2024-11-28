from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from product.models import Product, Transaction
from product.serializers import (
    ProductRegisterSerializer,
    TransactionSerializer,
    ProductSchema,
)


# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductRegisterSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return ProductRegisterSerializer
        return ProductSchema

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @action(methods=["POST"], detail=True)
    def purchase(self, request, pk):
        product = Product.objects.get(product_id=pk)

        if product.seller == request.user:
            return Response(
                {"error": "Seller can't buy his own product."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if product.status != "Available":
            return Response(
                {"error": "This item is not available now."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transaction = Transaction(product=product, buyer=request.user)
        transaction.save()

        return Response(TransactionSerializer(instance=transaction).data)

    @action(methods=["POST"], detail=True)
    def approve_sale(self, request, pk):
        product = self.get_object()

        if product.seller != request.user:
            return Response(
                {"error": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        transaction = product.transactions.filter(status="Pending").first()

        if not transaction:
            return Response(
                {"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND
            )

        transaction.status = "Approved"
        transaction.save()

        product.status = "Sold out"
        product.save()

        return Response(TransactionSerializer(instance=transaction).data)


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        purchased = Transaction.objects.filter(buyer=user)

        reserved = Transaction.objects.filter(
            (Q(buyer=user)) | Q(product__seller=user) & Q(product__status="Reserved")
        )

        return purchased.union(reserved)
