from django.db import models

from product.models import Transaction


# Create your models here.
class Payment(models.Model):
    transaction = models.ForeignKey(to=Transaction, on_delete=models.CASCADE)
    merchant_uid = models.CharField(max_length=40, verbose_name="고객사 주문번호")
    imp_uid = models.CharField(max_length=20, verbose_name="포트원 거래고유번호")
    amount = models.IntegerField(verbose_name="결제금액")
    status = models.CharField(max_length=10, verbose_name="결제상태")
    vbank_num = models.IntegerField(verbose_name="가상계좌 계좌번호")
    vbank_date = models.DateTimeField(verbose_name="가상계좌 입금기한")
    vbank_name = models.CharField(max_length=10, verbose_name="가상계좌 은행명")
    vbank_issued_at = models.CharField(max_length=10, verbose_name="가상계좌 생성시각")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
