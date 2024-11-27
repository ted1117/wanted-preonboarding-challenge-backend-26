from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Product(models.Model):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    SOLD_OUT = "Sold out"

    STATUS_CHOICES = [
        (AVAILABLE, "판매중"),
        (RESERVED, "예약중"),
        (SOLD_OUT, "판매완료"),
    ]

    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=False, null=False)
    price = models.IntegerField()
    seller = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="products"
    )
    status = models.CharField(choices=STATUS_CHOICES, default=AVAILABLE, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    PENDING = "Pending"
    APPROVED = "Approved"
    COMPLETED = "Completed"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        # (COMPLETED, "Completed"),
    ]

    transaction_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name="transactions"
    )
    buyer = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="purchases"
    )
    price_at_purchase = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction for {self.product.name} by {self.buyer.nickname}"

    def save(self, *args, **kwargs):
        self.price_at_purchase = self.product.price
        super().save()


# class TransactionLog(models.Model):
#     PENDING = "Pending"
#     APPROVED = "Approved"
#     COMPLETED = "Completed"
#
#     STATUS_CHOICES = [
#         (PENDING, "Pending"),
#         (APPROVED, "Approved"),
#         (COMPLETED, "Completed"),
#     ]
#
#     transaction_log_id = models.BigAutoField(primary_key=True)
#     transaction = models.ForeignKey(to=Transaction, on_delete=models.CASCADE)
#     status = models.CharField(choices=STATUS_CHOICES, default=PENDING)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
