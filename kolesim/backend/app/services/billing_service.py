import uuid

import httpx

from app.core.config import settings


async def create_yukassa_payment(amount: str, description: str, return_url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.yookassa.ru/v3/payments",
            auth=(settings.YUKASSA_SHOP_ID, settings.YUKASSA_SECRET_KEY),
            headers={"Idempotence-Key": str(uuid.uuid4())},
            json={
                "amount": {"value": amount, "currency": "RUB"},
                "description": description,
                "confirmation": {"type": "redirect", "return_url": return_url},
                "capture": True,
            },
            timeout=20,
        )
        response.raise_for_status()
        return response.json()
