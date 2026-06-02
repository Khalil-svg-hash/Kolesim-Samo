from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.models.media import Media
from app.models.place_accessibility import PlaceAccessibility
from app.models.places import Place
from app.models.reviews import Review
from app.utils.pagination import paginate


async def fetch_places(
    db: AsyncSession,
    filters: dict,
    page: int,
    limit: int,
    is_premium: bool,
) -> dict:
    accessibility = aliased(PlaceAccessibility)

    query = select(Place).outerjoin(accessibility, accessibility.place_id == Place.id)
    conditions = [Place.is_published.is_(True)]
    if not is_premium:
        conditions.append(Place.is_free.is_(True))

    if filters.get("category"):
        conditions.append(Place.category == filters["category"])
    if filters.get("city"):
        conditions.append(Place.city == filters["city"])
    if filters.get("is_verified") is not None:
        conditions.append(Place.is_verified.is_(filters["is_verified"]))
    if filters.get("has_elevator") is not None:
        conditions.append(accessibility.has_elevator.is_(filters["has_elevator"]))
    if filters.get("has_step_free_entrance") is not None:
        conditions.append(
            accessibility.has_step_free_entrance.is_(filters["has_step_free_entrance"])
        )
    if filters.get("has_accessible_wc") is not None:
        conditions.append(accessibility.has_accessible_wc.is_(filters["has_accessible_wc"]))
    if filters.get("has_accessible_parking") is not None:
        conditions.append(
            accessibility.has_accessible_parking.is_(filters["has_accessible_parking"])
        )
    if filters.get("min_door_width") is not None:
        conditions.append(
            accessibility.entrance_door_width_cm >= filters["min_door_width"]
        )
    if filters.get("price_levels"):
        conditions.append(Place.price_level.in_(filters["price_levels"]))
    if filters.get("search"):
        term = f"%{filters['search']}%"
        conditions.append(Place.name.ilike(term))

    query = query.where(and_(*conditions))
    count_query = (
        select(func.count())
        .select_from(Place)
        .outerjoin(accessibility, accessibility.place_id == Place.id)
        .where(and_(*conditions))
    )
    total = (await db.execute(count_query)).scalar_one()

    offset = (page - 1) * limit
    items = (await db.execute(query.offset(offset).limit(limit))).scalars().all()
    meta = paginate(total=total, page=page, limit=limit)

    if not items:
        return {"items": [], "accessibility": {}, "stats": {}, **meta}

    ids = [item.id for item in items]
    accessibility_rows = (
        await db.execute(
            select(PlaceAccessibility).where(PlaceAccessibility.place_id.in_(ids))
        )
    ).scalars().all()
    accessibility_map = {row.place_id: row for row in accessibility_rows}

    stats_rows = await db.execute(
        select(Review.entity_id, func.avg(Review.rating), func.count(Review.id))
        .where(Review.entity_id.in_(ids), Review.moderation_status == "approved")
        .group_by(Review.entity_id)
    )
    stats_map = {
        row[0]: {"avg_rating": float(row[1]) if row[1] else None, "review_count": row[2]}
        for row in stats_rows
    }

    return {"items": items, "accessibility": accessibility_map, "stats": stats_map, **meta}


async def fetch_place_detail(db: AsyncSession, place_id) -> dict | None:
    place = (await db.execute(select(Place).where(Place.id == place_id))).scalar_one_or_none()
    if not place:
        return None

    accessibility = (
        await db.execute(select(PlaceAccessibility).where(PlaceAccessibility.place_id == place.id))
    ).scalar_one_or_none()
    media = (await db.execute(select(Media).where(Media.entity_id == place.id))).scalars().all()
    stats = await db.execute(
        select(func.avg(Review.rating), func.count(Review.id)).where(
            Review.entity_id == place.id, Review.moderation_status == "approved"
        )
    )
    avg_rating, review_count = stats.one()
    return {
        "place": place,
        "accessibility": accessibility,
        "media": media,
        "avg_rating": float(avg_rating) if avg_rating else None,
        "review_count": review_count or 0,
    }
