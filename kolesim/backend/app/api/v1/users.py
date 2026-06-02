from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user_saved_places import UserSavedPlace
from app.models.user_saved_routes import UserSavedRoute
from app.schemas.users import UserResponse, UserUpdate
from app.services.storage_service import upload_file

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_me(
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)
    await db.flush()
    return current_user


@router.get("/me/saved-places")
async def saved_places(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    rows = (
        await db.execute(select(UserSavedPlace).where(UserSavedPlace.user_id == current_user.id))
    ).scalars().all()
    return {"items": [row.place_id for row in rows]}


@router.get("/me/saved-routes")
async def saved_routes(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    rows = (
        await db.execute(select(UserSavedRoute).where(UserSavedRoute.user_id == current_user.id))
    ).scalars().all()
    return {"items": [row.route_id for row in rows]}


@router.post("/me/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    file_bytes = await file.read()
    content_type = file.content_type or "application/octet-stream"
    try:
        url = await upload_file(file_bytes, content_type, folder="avatars")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    current_user.avatar_url = url
    await db.flush()
    return {"avatar_url": url}
