from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_admin_user
from app.models.places import Place
from app.models.routes import Route
from app.models.reviews import Review

router = APIRouter(dependencies=[Depends(get_admin_user)])


@router.get("/stats")
async def admin_stats(db: AsyncSession = Depends(get_db)):
    places = (await db.execute(select(func.count(Place.id)))).scalar_one()
    routes = (await db.execute(select(func.count(Route.id)))).scalar_one()
    reviews = (await db.execute(select(func.count(Review.id)))).scalar_one()
    return {"places": places, "routes": routes, "reviews": reviews}
