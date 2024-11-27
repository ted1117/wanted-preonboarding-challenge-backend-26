from django.contrib.auth import get_user_model
from rest_framework import serializers

from product.models import Product, Transaction

User = get_user_model()


class ProductRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "price"]


class ProductSchema(serializers.ModelSerializer):
    seller = serializers.StringRelatedField(read_only=True)
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "status",
            "seller",
            "transactions",
            "created_at",
            "updated_at",
        ]

    def get_transactions(self, obj):
        transactions = obj.transactions.all()
        return TransactionSerializer(instance=transactions, many=True).data


class TransactionSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField(read_only=True)
    depth = 1

    class Meta:
        model = Transaction
        fields = ["product", "buyer", "price_at_purchase", "status"]


# class TransactionLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TransactionLog
#         fields = "__all__"
