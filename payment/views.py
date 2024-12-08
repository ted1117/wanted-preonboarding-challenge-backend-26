import httpx
from django.shortcuts import render
from ninja import NinjaAPI
from ninja.responses import JsonResponse

from payment.models import Payment
from payment.services import get_token
from product.models import Product, Transaction

api = NinjaAPI()


# Create your views here.
@api.post("/webhook")
async def portone_webhook(request, payload: dict):
    try:
        if request.META.get("CONTENT_TYPE") == "application/json":
            merchant_uid = payload.get("merchant_uid")
            imp_uid = payload.get("imp_uid")
        else:
            merchant_uid = request.POST.get("merchant_uid")
            imp_uid = request.POST.get("imp_uid")

        if not imp_uid or not merchant_uid:
            return JsonResponse({"error": "Invalid data"}, status=400)

        access_token = get_token()

        async with httpx.AsyncClient() as client:
            payment_response = await client.get(
                f"https://api.iamport.kr/payments/{imp_uid}",
                headers={"Authorization": access_token},
            )

        payment_response.raise_for_status()
        payment_data = payment_response.json()["response"]

        try:
            payment = await Payment.objects.aget(
                transaction_id=payment_data["merchant_uid"]
            )
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment does not exist."}, status=404)

        amount_to_be_paid = payment.price_at_purchase

        if payment_data["amount"] == amount_to_be_paid:
            # transaction.status = Transaction.APPROVED
            # await transaction.asave()

            match payment_data["status"]:
                case "ready":
                    # payment.vbank_num = payment_data["vbank_num"]
                    # payment.vbank_name = payment_data["vbank_name"]
                    # payment.vbank_date = payment_data["vbank_date"]
                    # payment.vbank_issued_at = payment_data["vbank_issued_at"]
                    # payment.status = payment_data["status"]
                    # payment.asave()
                    pass

                case "paid":
                    pass

                case "failed":
                    pass

                case "cancelled":
                    pass

    except httpx.RequestError as e:
        return JsonResponse({"error": e}, status=400)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)
