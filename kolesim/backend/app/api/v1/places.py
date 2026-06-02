from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_admin_user, get_current_user, get_optional_user
from app.models.user_saved_places import UserSavedPlace
from app.models.place_accessibility import PlaceAccessibility
from app.models.places import Place
from app.schemas.places import PlaceCreate, PlaceListResponse, PlaceResponse, PlaceUpdate
from app.services.place_service import fetch_place_detail, fetch_places
from app.utils.slug import slugify

router = APIRouter()


@router.get("/", response_model=PlaceListResponse)
async def get_places(
    category: str | None = None,
    city: str | None = None,
    has_elevator: bool | None = None,
    has_step_free_entrance: bool | None = None,
    has_accessible_wc: bool | None = None,
    has_accessible_parking: bool | None = None,
    min_door_width: int | None = None,
    price_level: str | None = None,
    is_verified: bool | None = None,
    search: str | None = None,
    page: int = 1,
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_optional_user),
):
    is_premium = bool(current_user and current_user.subscription_status == "premium")
    price_levels = [int(x) for x in price_level.split(",")] if price_level else []
    payload = await fetch_places(
        db,
        {
            "category": category,
            "city": city,
            "has_elevator": has_elevator,
            "has_step_free_entrance": has_step_free_entrance,
            "has_accessible_wc": has_accessible_wc,
            "has_accessible_parking": has_accessible_parking,
            "min_door_width": min_door_width,
            "price_levels": price_levels,
            "is_verified": is_verified,
            "search": search,
        },
        page,
        limit,
        is_premium,
    )

    items = []
    for place in payload["items"]:
        stats = payload["stats"].get(place.id, {"avg_rating": None, "review_count": 0})
        response = PlaceResponse.model_validate(place)
        response.accessibility = payload["accessibility"].get(place.id)
        response.avg_rating = stats["avg_rating"]
        response.review_count = stats["review_count"]
        response.media = []
        items.append(response)

    return PlaceListResponse(
        items=items,
        total=payload["total"],
        page=payload["page"],
        limit=payload["limit"],
        pages=payload["pages"],
    )


@router.get("/{place_id}", response_model=PlaceResponse)
async def get_place(place_id: str, db: AsyncSession = Depends(get_db)):
    payload = await fetch_place_detail(db, place_id)
    if not payload:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")

    place = payload["place"]
    response = PlaceResponse.model_validate(place)
    response.accessibility = payload["accessibility"]
    response.media = payload["media"]
    response.avg_rating = payload["avg_rating"]
    response.review_count = payload["review_count"]
    return response


@router.post("/", response_model=PlaceResponse, dependencies=[Depends(get_admin_user)])
async def create_place(payload: PlaceCreate, db: AsyncSession = Depends(get_db)):
    slug = slugify(payload.name)
    place = Place(**payload.model_dump(exclude={"accessibility"}), slug=slug)
    db.add(place)
    await db.flush()

    if payload.accessibility:
        accessibility = PlaceAccessibility(
            place_id=place.id, **payload.accessibility.model_dump()
        )
        db.add(accessibility)

    response = PlaceResponse.model_validate(place)
    response.accessibility = payload.accessibility
    response.media = []
    response.avg_rating = None
    response.review_count = 0
    return response


@router.put("/{place_id}", response_model=PlaceResponse, dependencies=[Depends(get_admin_user)])
async def update_place(place_id: str, payload: PlaceUpdate, db: AsyncSession = Depends(get_db)):
    place = (await db.execute(select(Place).where(Place.id == place_id))).scalar_one_or_none()
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")

    for key, value in payload.model_dump(exclude={"accessibility"}).items():
        setattr(place, key, value)

    if payload.accessibility:
        accessibility = (
            await db.execute(
                select(PlaceAccessibility).where(PlaceAccessibility.place_id == place.id)
            )
        ).scalar_one_or_none()
        if accessibility:
            for key, value in payload.accessibility.model_dump().items():
                setattr(accessibility, key, value)
        else:
            db.add(PlaceAccessibility(place_id=place.id, **payload.accessibility.model_dump()))

    await db.flush()
    response = PlaceResponse.model_validate(place)
    response.accessibility = payload.accessibility
    response.media = []
    response.avg_rating = None
    response.review_count = 0
    return response


@router.delete("/{place_id}", dependencies=[Depends(get_admin_user)])
async def delete_place(place_id: str, db: AsyncSession = Depends(get_db)):
    place = (await db.execute(select(Place).where(Place.id == place_id))).scalar_one_or_none()
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")
    await db.delete(place)
    return {"status": "ok"}


@router.post("/{place_id}/save")
async def save_place(place_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    place = (await db.execute(select(Place).where(Place.id == place_id))).scalar_one_or_none()
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")
    existing = (
        await db.execute(
            select(UserSavedPlace).where(
                UserSavedPlace.user_id == current_user.id,
                UserSavedPlace.place_id == place.id,
            )
        )
    ).scalar_one_or_none()
    if not existing:
        db.add(UserSavedPlace(user_id=current_user.id, place_id=place.id))
        await db.flush()
    return {"status": "ok"}


@router.delete("/{place_id}/save")
async def unsave_place(
    place_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    saved = (
        await db.execute(
            select(UserSavedPlace).where(
                UserSavedPlace.user_id == current_user.id,
                UserSavedPlace.place_id == place_id,
            )
        )
    ).scalar_one_or_none()
    if saved:
        await db.delete(saved)
    return {"status": "ok"}
