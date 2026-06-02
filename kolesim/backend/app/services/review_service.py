from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.media import Media
from app.models.places import Place
from app.models.reviews import Review
from app.models.routes import Route
from app.services.storage_service import upload_file


async def create_review(
    db: AsyncSession,
    payload: dict,
    user_id,
    files: list[tuple[bytes, str]] | None = None,
) -> Review:
    entity_type = payload["entity_type"]
    entity_id = payload["entity_id"]

    if entity_type == "place":
        exists = await db.execute(select(Place).where(Place.id == entity_id))
    else:
        exists = await db.execute(select(Route).where(Route.id == entity_id))

    if not exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")

    review = Review(**payload, user_id=user_id, moderation_status="pending")
    db.add(review)
    await db.flush()

    if files:
        for index, (file_bytes, content_type) in enumerate(files):
            url = await upload_file(file_bytes, content_type, folder="reviews")
            db.add(
                Media(
                    entity_type="review",
                    entity_id=review.id,
                    url=url,
                    media_type="photo",
                    sort_order=index,
                )
            )

    return review


async def moderate_review(db: AsyncSession, review_id, status_value: str, note: str | None):
    review = (await db.execute(select(Review).where(Review.id == review_id))).scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отзыв не найден")
    review.moderation_status = status_value
    review.moderation_note = note
    await db.flush()
    return review
