from datetime import timedelta
import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models.users import User


async def register_user(db: AsyncSession, email: str, password: str, full_name: str | None) -> User:
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email уже зарегистрирован")

    user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name,
    )
    db.add(user)
    await db.flush()
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные учетные данные")
    return user


def build_token_payload(user: User) -> dict:
    return {"sub": str(user.id), "email": user.email, "is_admin": user.is_admin}


def issue_tokens(user: User) -> dict:
    payload = build_token_payload(user)
    access_token = create_access_token(payload)
    refresh_payload = {**payload, "jti": str(uuid.uuid4())}
    refresh_token = create_refresh_token(refresh_payload)
    return {"access_token": access_token, "refresh_token": refresh_token}


def build_verify_token(user: User) -> str:
    payload = {"sub": str(user.id), "purpose": "verify"}
    return create_access_token(payload, expires_delta=timedelta(hours=24))


def build_reset_token(user: User) -> str:
    payload = {"sub": str(user.id), "purpose": "reset"}
    return create_access_token(payload, expires_delta=timedelta(hours=1))
