from django.conf import settings
import requests


def get_token():
    response = requests.post(
        "https://api.iamport.kr/users/getToken/",
        json={"imp_key": settings.IMP_KEY, "imp_secret": settings.IMP_SECRET},
    )

    response.raise_for_status()
    access_token = response.json()["response"]["access_token"]

    return access_token
