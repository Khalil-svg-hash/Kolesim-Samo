from random import sample

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.place_accessibility import PlaceAccessibility
from app.models.places import Place
from app.models.route_places import RoutePlace
from app.models.routes import Route
from app.utils.pagination import paginate


async def fetch_routes(db: AsyncSession, is_premium: bool, page: int, limit: int) -> dict:
    query = select(Route).where(Route.is_published.is_(True))
    if not is_premium:
        query = query.where(Route.is_free.is_(True))

    total = (
        await db.execute(select(func.count()).select_from(query.subquery()))
    ).scalar_one()
    offset = (page - 1) * limit
    items = (await db.execute(query.offset(offset).limit(limit))).scalars().all()
    meta = paginate(total=total, page=page, limit=limit)
    return {"items": items, **meta}


async def construct_route(db: AsyncSession, filters: dict) -> list[dict]:
    accessibility = select(Place).join(PlaceAccessibility, PlaceAccessibility.place_id == Place.id)
    conditions = [Place.is_published.is_(True), Place.is_verified.is_(True)]
    if filters.get("has_elevator") is not None:
        conditions.append(PlaceAccessibility.has_elevator.is_(filters["has_elevator"]))
    if filters.get("has_accessible_wc") is not None:
        conditions.append(PlaceAccessibility.has_accessible_wc.is_(filters["has_accessible_wc"]))
    if filters.get("min_door_width") is not None:
        conditions.append(PlaceAccessibility.entrance_door_width_cm >= filters["min_door_width"])
    if filters.get("city"):
        conditions.append(Place.city == filters["city"])

    place_query = accessibility.where(*conditions)
    places = (await db.execute(place_query)).scalars().all()

    editorial_query = select(Route).where(Route.is_editorial.is_(True), Route.is_published.is_(True))
    if filters.get("tags"):
        editorial_query = editorial_query.where(Route.tags.overlap(filters["tags"]))
    editorials = (await db.execute(editorial_query)).scalars().all()

    responses = []
    for editorial in editorials:
        route_places = (
            await db.execute(
                select(RoutePlace)
                .where(RoutePlace.route_id == editorial.id)
                .order_by(RoutePlace.order_index)
            )
        ).scalars().all()
        place_ids = [rp.place_id for rp in route_places]
        if place_ids:
            place_rows = (
                await db.execute(select(Place).where(Place.id.in_(place_ids)))
            ).scalars().all()
            place_map = {place.id: place for place in place_rows}
            ordered_places = [place_map.get(place_id) for place_id in place_ids if place_map.get(place_id)]
        else:
            ordered_places = []
        responses.append({"route": editorial, "places": ordered_places})

    if responses:
        return responses

    if not places:
        return []

    picks = sample(places, min(len(places), 5))
    return [{"route": None, "places": picks}]
