from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.subscriptions import Subscription
from app.models.users import User
from app.schemas.billing import SubscribeRequest, SubscribeResponse
from app.services.billing_service import create_yukassa_payment

router = APIRouter()


@router.post("/subscribe", response_model=SubscribeResponse)
async def subscribe(payload: SubscribeRequest, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    amount = "299.00" if payload.plan == "monthly" else "2990.00"
    payment = await create_yukassa_payment(
        amount=amount,
        description=f"Подписка {payload.plan}",
        return_url=settings.YUKASSA_RETURN_URL,
    )
    started_at = datetime.utcnow()
    expires_at = started_at + timedelta(days=30 if payload.plan == "monthly" else 365)
    sub = Subscription(
        user_id=current_user.id,
        plan=payload.plan,
        status="pending",
        amount_rub=float(amount),
        started_at=started_at,
        expires_at=expires_at,
        provider_payment_id=payment.get("id"),
    )
    db.add(sub)
    await db.flush()
    confirmation = payment.get("confirmation") or {}
    url = confirmation.get("confirmation_url")
    if not url:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Ошибка платежа")
    return SubscribeResponse(payment_url=url)


def _trusted_webhook(request: Request) -> bool:
    if settings.ENVIRONMENT != "production":
        return True
    allowlist = {ip.strip() for ip in settings.YUKASSA_TRUSTED_IPS.split(",") if ip.strip()}
    if not allowlist:
        return True
    client_ip = request.client.host if request.client else ""
    return client_ip in allowlist


@router.post("/webhook")
async def webhook(request: Request, db: AsyncSession = Depends(get_db)):
    if not _trusted_webhook(request):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недоверенный источник")
    payload = await request.json()
    event = payload.get("event")
    payment_obj = payload.get("object") or {}
    payment_id = payment_obj.get("id")
    if not payment_id:
        return {"status": "ignored"}

    sub = (
        await db.execute(select(Subscription).where(Subscription.provider_payment_id == payment_id))
    ).scalar_one_or_none()
    if not sub:
        return {"status": "ignored"}

    if event == "payment.succeeded":
        sub.status = "active"
        user = (
            await db.execute(select(User).where(User.id == sub.user_id))
        ).scalar_one_or_none()
        if user:
            user.subscription_status = "premium"
    elif event == "payment.canceled":
        await db.delete(sub)

    return {"status": "ok"}
