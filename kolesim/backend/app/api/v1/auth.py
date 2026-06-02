from datetime import timedelta
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.redis import redis_client
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.models.users import User
from app.schemas.users import UserCreate, UserLogin, UserResponse
from app.services.auth_service import (
    authenticate_user,
    build_reset_token,
    build_verify_token,
    issue_tokens,
    register_user,
)
from app.utils.email import send_email

router = APIRouter()

ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        ACCESS_COOKIE,
        access_token,
        httponly=True,
        samesite="lax",
        secure=settings.ENVIRONMENT == "production",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        REFRESH_COOKIE,
        refresh_token,
        httponly=True,
        samesite="lax",
        secure=settings.ENVIRONMENT == "production",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )


def _clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(ACCESS_COOKIE)
    response.delete_cookie(REFRESH_COOKIE)


@router.post("/register")
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await register_user(db, payload.email, payload.password, payload.full_name)
    token = build_verify_token(user)
    verify_url = f"{settings.FRONTEND_URL}/api/v1/auth/verify-email/{token}"
    await send_email(
        user.email,
        "Подтверждение email",
        f"<p>Подтвердите email: <a href='{verify_url}'>ссылка</a></p>",
    )
    return {"message": f"Письмо с подтверждением отправлено на {user.email}"}


@router.post("/login", response_model=UserResponse)
async def login(response: Response, payload: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, payload.email, payload.password)
    tokens = issue_tokens(user)
    _set_auth_cookies(response, tokens["access_token"], tokens["refresh_token"])
    return user


@router.post("/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get(REFRESH_COOKIE)
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Нет refresh токена")

    if await redis_client.get(f"bl:{refresh_token}"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен отозван")

    payload = decode_token(refresh_token)
    if payload.get("jti") is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный токен")

    access_token = create_access_token(
        {"sub": payload.get("sub"), "email": payload.get("email"), "is_admin": payload.get("is_admin")}
    )
    new_jti = str(uuid.uuid4())
    rotated_refresh = create_refresh_token(
        {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "is_admin": payload.get("is_admin"),
            "jti": new_jti,
        },
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    await redis_client.setex(
        f"bl:{refresh_token}",
        settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        "1",
    )
    _set_auth_cookies(response, access_token, rotated_refresh)
    return {"status": "ok"}


@router.post("/logout")
async def logout(request: Request, response: Response):
    refresh_token = request.cookies.get(REFRESH_COOKIE)
    if refresh_token:
        await redis_client.setex(
            f"bl:{refresh_token}", settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60, "1"
        )
    _clear_auth_cookies(response)
    return {"status": "ok"}


@router.get("/verify-email/{token}")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if payload.get("purpose") != "verify":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный токен")

    user = (
        await db.execute(select(User).where(User.id == payload.get("sub")))
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    user.is_verified = True
    await db.flush()
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?verified=true")


@router.post("/forgot-password")
async def forgot_password(payload: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == payload.email))).scalar_one_or_none()
    if user:
        token = build_reset_token(user)
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        await send_email(
            user.email,
            "Сброс пароля",
            f"<p>Ссылка для сброса: <a href='{reset_url}'>ссылка</a></p>",
        )
    return {"status": "ok"}


@router.post("/reset-password")
async def reset_password(payload: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    decoded = decode_token(payload.token)
    if decoded.get("purpose") != "reset":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный токен")

    user = (
        await db.execute(select(User).where(User.id == decoded.get("sub")))
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    from app.core.security import hash_password

    user.hashed_password = hash_password(payload.new_password)
    await db.flush()
    return {"status": "ok"}
