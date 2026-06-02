from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_admin_user, get_current_user
from app.schemas.reviews import ReviewCreate, ReviewModerate, ReviewResponse
from app.services.review_service import create_review, moderate_review

router = APIRouter()


@router.post("/", response_model=ReviewResponse)
async def create_review_endpoint(
    payload: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    files: list[UploadFile] | None = File(default=None),
):
    file_payloads = []
    if files:
        for file in files[:5]:
            file_bytes = await file.read()
            file_payloads.append((file_bytes, file.content_type or "application/octet-stream"))
    review = await create_review(
        db,
        payload.model_dump(),
        current_user.id,
        file_payloads,
    )
    return ReviewResponse.model_validate(review)


@router.patch("/{review_id}/moderate", response_model=ReviewResponse, dependencies=[Depends(get_admin_user)])
async def moderate_review_endpoint(
    review_id: str,
    payload: ReviewModerate,
    db: AsyncSession = Depends(get_db),
):
    review = await moderate_review(db, review_id, payload.status, payload.note)
    return ReviewResponse.model_validate(review)
