"""Seed script for development data."""
import asyncio
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.models import (
    Media,
    Place,
    PlaceAccessibility,
    Review,
    Route,
    RoutePlace,
    Subscription,
    User,
)


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        # ── Admin user ──────────────────────────────────────────
        admin_id = uuid.uuid4()
        result = await db.execute(select(User).where(User.email == "admin@kolesim.ru"))
        if not result.scalar_one_or_none():
            admin = User(
                id=admin_id,
                email="admin@kolesim.ru",
                full_name="Админ",
                hashed_password=hash_password("admin123"),
                is_verified=True,
                is_admin=True,
                subscription_status="premium",
            )
            db.add(admin)
            await db.flush()
            admin_id = admin.id
        else:
            admin_id = (await db.execute(select(User).where(User.email == "admin@kolesim.ru"))).scalar_one().id

        # ── Demo user ───────────────────────────────────────────
        demo_id = uuid.uuid4()
        result = await db.execute(select(User).where(User.email == "demo@kolesim.ru"))
        if not result.scalar_one_or_none():
            demo = User(
                id=demo_id,
                email="demo@kolesim.ru",
                full_name="Демо Пользователь",
                hashed_password=hash_password("demo1234"),
                is_verified=True,
                subscription_status="free",
            )
            db.add(demo)
            await db.flush()
            demo_id = demo.id
        else:
            demo_id = (await db.execute(select(User).where(User.email == "demo@kolesim.ru"))).scalar_one().id

        # ── Places ──────────────────────────────────────────────
        places_data = [
            {
                "name": "Государственный музей изобразительных искусств им. А.С. Пушкина",
                "slug": "pushkin-museum",
                "description": "Один из крупнейших музеев изобразительного искусства в России.",
                "category": "attraction",
                "address": "ул. Волхонка, 12, Москва",
                "city": "Москва",
                "latitude": 55.7475,
                "longitude": 37.6047,
                "price_level": 2,
                "is_verified": True,
                "is_free": False,
                "is_published": True,
            },
            {
                "name": "Парк Горького",
                "slug": "gorky-park",
                "description": "Центральный парк культуры и отдыха с доступной инфраструктурой.",
                "category": "attraction",
                "address": "Крымский Вал, 9, Москва",
                "city": "Москва",
                "latitude": 55.7296,
                "longitude": 37.6009,
                "price_level": 1,
                "is_verified": True,
                "is_free": True,
                "is_published": True,
            },
            {
                "name": "Ресторан Белуга",
                "slug": "beluga-restaurant",
                "description": "Ресторан русской кухни с полной доступностью для колясочников.",
                "category": "restaurant",
                "address": "Раушская наб., 4, Москва",
                "city": "Москва",
                "latitude": 55.7486,
                "longitude": 37.6292,
                "price_level": 3,
                "is_verified": True,
                "is_free": False,
                "is_published": True,
            },
            {
                "name": "Отель Метрополь",
                "slug": "metropol-hotel",
                "description": "Исторический отель с доступными номерами и удобным расположением.",
                "category": "hotel",
                "address": "Театральный пр-д, 2, Москва",
                "city": "Москва",
                "latitude": 55.7580,
                "longitude": 37.6173,
                "price_level": 3,
                "is_verified": True,
                "is_free": False,
                "is_published": True,
            },
            {
                "name": "Станция метро «Парк Победы»",
                "slug": "metro-park-pobedy",
                "description": "Станция с лифтами и доступной средой для маломобильных граждан.",
                "category": "transport",
                "address": "Площадь Победы, Москва",
                "city": "Москва",
                "latitude": 55.7355,
                "longitude": 37.5163,
                "price_level": 1,
                "is_verified": True,
                "is_free": False,
                "is_published": True,
            },
        ]

        place_ids: list[uuid.UUID] = []
        for pd in places_data:
            result = await db.execute(select(Place).where(Place.slug == pd["slug"]))
            existing = result.scalar_one_or_none()
            if existing:
                place_ids.append(existing.id)
                continue
            place = Place(**pd)
            db.add(place)
            await db.flush()
            place_ids.append(place.id)

        # ── Accessibility ───────────────────────────────────────
        acc_data = [
            {"has_step_free_entrance": True, "entrance_door_width_cm": 90, "has_ramp": True, "has_elevator": True, "elevator_door_width_cm": 80, "has_accessible_wc": True, "wc_door_width_cm": 85, "has_accessible_parking": True, "parking_distance_m": 50, "floor_surface": "tile", "extra_notes": "Полная доступность"},
            {"has_step_free_entrance": True, "entrance_door_width_cm": 120, "has_ramp": True, "has_elevator": False, "elevator_door_width_cm": None, "has_accessible_wc": True, "wc_door_width_cm": 90, "has_accessible_parking": True, "parking_distance_m": 30, "floor_surface": "asphalt", "extra_notes": "Открытая территория, ровные дорожки"},
            {"has_step_free_entrance": True, "entrance_door_width_cm": 100, "has_ramp": True, "has_elevator": True, "elevator_door_width_cm": 85, "has_accessible_wc": True, "wc_door_width_cm": 85, "has_accessible_parking": True, "parking_distance_m": 20, "floor_surface": "tile", "extra_notes": "Полная доступность"},
            {"has_step_free_entrance": True, "entrance_door_width_cm": 110, "has_ramp": True, "has_elevator": True, "elevator_door_width_cm": 90, "has_accessible_wc": True, "wc_door_width_cm": 90, "has_accessible_parking": True, "parking_distance_m": 15, "floor_surface": "carpet", "extra_notes": "Доступные номера на первом этаже"},
            {"has_step_free_entrance": True, "entrance_door_width_cm": 100, "has_ramp": True, "has_elevator": True, "elevator_door_width_cm": 90, "has_accessible_wc": False, "wc_door_width_cm": None, "has_accessible_parking": True, "parking_distance_m": 10, "floor_surface": "tile", "extra_notes": "Лифт от платформы до выхода"},
        ]

        for i, place_id in enumerate(place_ids):
            result = await db.execute(
                select(PlaceAccessibility).where(PlaceAccessibility.place_id == place_id)
            )
            if not result.scalar_one_or_none() and i < len(acc_data):
                acc = PlaceAccessibility(place_id=place_id, **acc_data[i])
                db.add(acc)

        await db.flush()

        # ── Route ───────────────────────────────────────────────
        route_slug = "moscow-center-1day"
        result = await db.execute(select(Route).where(Route.slug == route_slug))
        route = result.scalar_one_or_none()
        if not route:
            route = Route(
                title="Москва за день: доступный маршрут",
                slug=route_slug,
                description="Однодневный маршрут по главным доступным достопримечательностям центра Москвы.",
                duration_days=1,
                distance_km=8.5,
                difficulty="easy",
                tags=["музеи", "парки", "рестораны"],
                is_editorial=True,
                is_published=True,
                is_free=True,
                created_by=admin_id,
            )
            db.add(route)
            await db.flush()

            for idx, place_id in enumerate(place_ids[:3]):
                rp = RoutePlace(
                    route_id=route.id,
                    place_id=place_id,
                    order_index=idx + 1,
                    day_number=1,
                    notes="Основная точка маршрута",
                    estimated_duration_min=90,
                )
                db.add(rp)

        await db.flush()

        # ── Reviews ─────────────────────────────────────────────
        for i, place_id in enumerate(place_ids[:3]):
            result = await db.execute(
                select(Review).where(Review.entity_id == place_id, Review.user_id == demo_id)
            )
            if not result.scalar_one_or_none():
                review = Review(
                    user_id=demo_id,
                    entity_type="place",
                    entity_id=place_id,
                    rating=4 + (i % 2),
                    accessibility_rating=4,
                    text="Хорошая доступность, рекомендую.",
                    wheelchair_type="manual",
                    moderation_status="approved",
                )
                db.add(review)

        await db.commit()
        print("✅ Seed completed successfully")


if __name__ == "__main__":
    asyncio.run(seed())