from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from reportlab.graphics.barcode import qr
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_admin_user, get_current_user, get_optional_user, get_premium_user
from app.models.places import Place
from app.models.route_places import RoutePlace
from app.models.routes import Route
from app.models.user_saved_routes import UserSavedRoute
from app.schemas.routes import RouteConstructResponse, RouteListResponse, RouteResponse
from app.services.route_service import construct_route, fetch_routes

router = APIRouter()


@router.get("/construct", response_model=list[RouteConstructResponse])
async def construct_route_endpoint(
    duration_days: int = Query(1, ge=1, le=2),
    tags: str | None = None,
    has_elevator: bool | None = None,
    has_accessible_wc: bool | None = None,
    min_door_width: int | None = None,
    city: str = "Москва",
    current_user=Depends(get_premium_user),
    db: AsyncSession = Depends(get_db),
):
    filters = {
        "duration_days": duration_days,
        "tags": [tag.strip() for tag in tags.split(",")] if tags else None,
        "has_elevator": has_elevator,
        "has_accessible_wc": has_accessible_wc,
        "min_door_width": min_door_width,
        "city": city,
    }
    routes = await construct_route(db, filters)
    responses = []
    for entry in routes:
        route_obj = entry["route"]
        response_route = RouteResponse.model_validate(route_obj) if route_obj else None
        responses.append(
            RouteConstructResponse(
                route=response_route,
                places=entry["places"],
                estimated_distance_km=None,
            )
        )
    return responses


@router.get("/", response_model=RouteListResponse)
async def list_routes(
    page: int = 1,
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_optional_user),
):
    is_premium = bool(current_user and current_user.subscription_status == "premium")
    payload = await fetch_routes(db, is_premium, page, limit)
    return RouteListResponse(**payload)


@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(route_id: str, db: AsyncSession = Depends(get_db)):
    route = (await db.execute(select(Route).where(Route.id == route_id))).scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маршрут не найден")
    return RouteResponse.model_validate(route)


@router.get("/{route_id}/export-pdf")
async def export_route_pdf(route_id: str, db: AsyncSession = Depends(get_db)):
    route = (await db.execute(select(Route).where(Route.id == route_id))).scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маршрут не найден")

    route_places = (
        await db.execute(
            select(RoutePlace)
            .where(RoutePlace.route_id == route.id)
            .order_by(RoutePlace.order_index)
        )
    ).scalars().all()
    place_ids = [rp.place_id for rp in route_places]
    places = []
    if place_ids:
        places = (
            await db.execute(select(Place).where(Place.id.in_(place_ids)))
        ).scalars().all()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setTitle(route.title)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(2 * cm, height - 2 * cm, route.title)

    pdf.setFont("Helvetica", 11)
    y = height - 3 * cm
    if route.description:
        pdf.drawString(2 * cm, y, route.description[:120])
        y -= 1 * cm

    pdf.drawString(2 * cm, y, f"Длительность: {route.duration_days} дн.")
    y -= 0.7 * cm
    if route.tags:
        pdf.drawString(2 * cm, y, f"Теги: {', '.join(route.tags)}")
        y -= 0.7 * cm

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(2 * cm, y, "Места маршрута:")
    y -= 0.8 * cm
    pdf.setFont("Helvetica", 11)

    for index, place in enumerate(places, start=1):
        line = f"{index}. {place.name} — {place.address}"
        pdf.drawString(2 * cm, y, line[:110])
        y -= 0.6 * cm
        if y < 4 * cm:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = height - 2 * cm

    route_url = f"https://kolesim.ru/routes/{route.slug}"
    qr_code = qr.QrCodeWidget(route_url)
    bounds = qr_code.getBounds()
    size = 4 * cm
    width_qr = bounds[2] - bounds[0]
    height_qr = bounds[3] - bounds[1]
    d = min(size / width_qr, size / height_qr)
    qr_code.drawOn(pdf, width - 6 * cm, 2 * cm, d)

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    filename = f"route-{route.slug or route.id}.pdf"
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.delete("/{route_id}", dependencies=[Depends(get_admin_user)])
async def delete_route(route_id: str, db: AsyncSession = Depends(get_db)):
    route = (await db.execute(select(Route).where(Route.id == route_id))).scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маршрут не найден")
    await db.delete(route)
    return {"status": "ok"}


@router.post("/{route_id}/save")
async def save_route(route_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    route = (await db.execute(select(Route).where(Route.id == route_id))).scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маршрут не найден")
    existing = (
        await db.execute(
            select(UserSavedRoute).where(
                UserSavedRoute.user_id == current_user.id,
                UserSavedRoute.route_id == route.id,
            )
        )
    ).scalar_one_or_none()
    if not existing:
        db.add(UserSavedRoute(user_id=current_user.id, route_id=route.id))
        await db.flush()
    return {"status": "ok"}


@router.delete("/{route_id}/save")
async def unsave_route(
    route_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    saved = (
        await db.execute(
            select(UserSavedRoute).where(
                UserSavedRoute.user_id == current_user.id,
                UserSavedRoute.route_id == route_id,
            )
        )
    ).scalar_one_or_none()
    if saved:
        await db.delete(saved)
    return {"status": "ok"}
