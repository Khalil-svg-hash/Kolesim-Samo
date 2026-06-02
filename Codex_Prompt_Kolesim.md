# Промпт для ChatGPT Codex: «Колесим самостоятельно»
> Скопируй этот промпт целиком в ChatGPT Codex / Cursor / Claude Code

---

## СИСТЕМНЫЙ ПРОМПТ (вставляй в System / Instructions)

Ты — опытный full-stack разработчик. Тебе нужно создать с нуля веб-платформу **«Колесим самостоятельно»** — каталог проверенных доступных мест и конструктор маршрутов для пользователей инвалидной коляски по Москве и Московской области.

**Строго следуй этому стеку:**
- Backend: Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic v2, PostgreSQL 15
- Frontend: TypeScript, Next.js 14 (App Router), React, Tailwind CSS, shadcn/ui, React Query v5, Zustand, React-Leaflet
- Инфраструктура: Docker Compose, Nginx, Redis

**Принципы:**
1. Пиши production-качественный код — не заглушки и не TODO.
2. Каждый файл должен быть полным и рабочим.
3. Используй async/await везде в backend.
4. Обрабатывай все ошибки явно (не голые except).
5. Валидируй входные данные через Pydantic (backend) и Zod (frontend).
6. Интерфейс соответствует WCAG 2.1 AA (aria-labels, alt-тексты, focus management).
7. Весь интерфейс на русском языке.
8. Не используй localStorage — только httpOnly cookies для токенов.

---

## ЗАДАЧА 1: ИНИЦИАЛИЗАЦИЯ ПРОЕКТА

Создай следующую структуру проекта:

```
kolesim/
├── backend/
├── frontend/
├── nginx/
├── docker-compose.yml
├── docker-compose.prod.yml
└── .env.example
```

### 1.1 docker-compose.yml

Создай `docker-compose.yml` со следующими сервисами:
- `db`: postgres:15-alpine, volume postgres_data, healthcheck через pg_isready
- `redis`: redis:7-alpine
- `backend`: build ./backend, зависит от db + redis, порт 8000
- `frontend`: build ./frontend, зависит от backend, порт 3000
- `nginx`: nginx:alpine, порты 80/443, конфиг из ./nginx/nginx.conf

Все секреты — через переменные окружения из .env файла.

### 1.2 .env.example

```env
DB_PASSWORD=changeme
SECRET_KEY=your-256-bit-secret
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
SMTP_HOST=smtp.yandex.ru
SMTP_PORT=465
SMTP_USER=noreply@kolesim.ru
SMTP_PASSWORD=changeme
YUKASSA_SHOP_ID=your_shop_id
YUKASSA_SECRET_KEY=your_secret
YUKASSA_RETURN_URL=https://kolesim.ru/billing/success
S3_BUCKET=kolesim-media
S3_ACCESS_KEY=changeme
S3_SECRET_KEY=changeme
S3_ENDPOINT=https://storage.yandexcloud.net
S3_REGION=ru-central1
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
REDIS_URL=redis://redis:6379/0
```

### 1.3 nginx/nginx.conf

```nginx
events { worker_connections 1024; }
http {
  upstream backend { server backend:8000; }
  upstream frontend { server frontend:3000; }

  server {
    listen 80;
    server_name localhost;

    location /api/ {
      proxy_pass http://backend;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location / {
      proxy_pass http://frontend;
      proxy_set_header Host $host;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
    }
  }
}
```

---

## ЗАДАЧА 2: BACKEND

### 2.1 Зависимости (backend/requirements.txt)

```
fastapi==0.111.0
uvicorn[standard]==0.30.1
sqlalchemy[asyncio]==2.0.31
asyncpg==0.29.0
alembic==1.13.2
pydantic==2.8.2
pydantic-settings==2.3.4
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
fastapi-mail==1.4.1
boto3==1.34.144
httpx==0.27.0
redis[hiredis]==5.0.7
python-dotenv==1.0.1
pytest==8.3.2
pytest-asyncio==0.23.8
httpx==0.27.0
```

### 2.2 backend/app/core/config.py

Создай `Settings` класс на основе `pydantic_settings.BaseSettings`:

```python
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    FRONTEND_URL: str = "http://localhost:3000"
    ENVIRONMENT: str = "development"
    
    SMTP_HOST: str
    SMTP_PORT: int = 465
    SMTP_USER: str
    SMTP_PASSWORD: str
    
    YUKASSA_SHOP_ID: str = ""
    YUKASSA_SECRET_KEY: str = ""
    YUKASSA_RETURN_URL: str = ""
    
    S3_BUCKET: str = ""
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_ENDPOINT: str = "https://storage.yandexcloud.net"
    S3_REGION: str = "ru-central1"

    class Config:
        env_file = ".env"

settings = Settings()
```

### 2.3 backend/app/core/database.py

Создай async SQLAlchemy engine и session factory:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### 2.4 backend/app/models/ — Все модели

Создай **полные** SQLAlchemy 2.0 ORM-модели для следующих таблиц. Каждый файл должен импортировать `Base` из `app.core.database`.

**users.py:**
- id: UUID primary key (default gen_random_uuid)
- email: String(255) unique not null
- hashed_password: String(255) not null
- full_name: String(255) nullable
- avatar_url: Text nullable
- wheelchair_type: String(50) nullable — manual | electric | child | unknown
- min_door_width_cm: Integer default 60
- needs_accessible_wc: Boolean default False
- is_active: Boolean default True
- is_verified: Boolean default False
- is_admin: Boolean default False
- subscription_status: String(50) default 'free' — free | premium
- subscription_expires_at: DateTime(timezone=True) nullable
- created_at / updated_at: DateTime(timezone=True)

**places.py:**
- id, name, slug (unique), description, category, address, city (default 'Москва')
- latitude, longitude: Numeric(10, 8)/(11, 8) not null
- entrance_lat, entrance_lng: Numeric nullable (GPS входа)
- parking_lat, parking_lng: Numeric nullable (GPS парковки)
- price_level: SmallInteger 1–3 nullable
- is_free_entry: Boolean default False
- working_hours: JSON nullable
- phone, website_url: nullable
- is_verified: Boolean default False
- verified_at: DateTime nullable
- verified_by: FK → users.id nullable
- is_free: Boolean default False (freemium)
- is_published: Boolean default False
- created_by: FK → users.id nullable
- created_at / updated_at

**place_accessibility.py:**
- id, place_id (FK → places.id, unique, cascade delete)
- has_step_free_entrance: Boolean nullable
- entrance_door_width_cm: Integer nullable
- has_ramp: Boolean nullable
- ramp_angle_deg: Numeric(4,1) nullable
- has_elevator: Boolean nullable
- elevator_door_width_cm: Integer nullable
- elevator_notes: Text nullable
- has_accessible_wc: Boolean nullable
- wc_door_width_cm: Integer nullable
- wc_notes: Text nullable
- has_accessible_parking: Boolean nullable
- parking_distance_m: Integer nullable
- floor_surface: String(100) nullable — asphalt | tile | gravel | cobblestone | mixed
- extra_notes: Text nullable
- last_checked_at: DateTime nullable
- checked_by: FK → users.id nullable
- created_at / updated_at

**media.py:**
- id, entity_type (String 50), entity_id (UUID не FK — полиморфный), url, thumbnail_url, caption, media_type (default 'photo'), sort_order (default 0), uploaded_by FK → users nullable, created_at

**routes.py:**
- id, title, slug (unique), description
- duration_days: SmallInteger default 1 (CHECK 1–2)
- distance_km: Numeric(6,2) nullable
- difficulty: String(50) nullable — easy | medium | hard
- tags: ARRAY(String) nullable
- is_editorial: Boolean default False
- is_published: Boolean default False
- is_free: Boolean default False
- view_count: Integer default 0
- created_by: FK → users.id nullable
- created_at / updated_at

**route_places.py:**
- id, route_id FK → routes.id (cascade), place_id FK → places.id
- order_index: Integer not null
- day_number: SmallInteger default 1
- notes: Text nullable
- estimated_duration_min: Integer nullable
- Unique constraint: (route_id, order_index)

**reviews.py:**
- id, user_id FK → users.id
- entity_type: String(50) — place | route
- entity_id: UUID
- rating: SmallInteger CHECK 1–5
- accessibility_rating: SmallInteger CHECK 1–5
- text: Text nullable
- visited_at: Date nullable
- wheelchair_type: String(50) nullable
- moderation_status: String(50) default 'pending' — pending | approved | rejected
- moderation_note: Text nullable
- moderated_by FK → users nullable
- moderated_at: DateTime nullable
- created_at

**subscriptions.py:**
- id, user_id FK → users.id
- plan: String(50) — monthly | annual
- status: String(50) — active | cancelled | expired
- payment_provider: String(50) default 'yukassa'
- provider_payment_id: String(255) nullable
- amount_rub: Numeric(10,2)
- started_at / expires_at / cancelled_at / created_at

**user_saved_places.py и user_saved_routes.py:**
- Ассоциативные таблицы: user_id + place_id/route_id (composite PK), created_at

### 2.5 backend/app/core/security.py

Реализуй:
- `hash_password(password: str) -> str` — bcrypt cost 12
- `verify_password(plain: str, hashed: str) -> bool`
- `create_access_token(data: dict) -> str` — expire из settings
- `create_refresh_token(data: dict) -> str`
- `decode_token(token: str) -> dict` — JWTError → HTTPException 401

### 2.6 backend/app/core/dependencies.py

Реализуй dependency injection:
- `get_db()` — async generator, уже реализован в database.py
- `get_current_user(db, token from cookie/header) -> User` — проверяет JWT, возвращает User из БД
- `get_current_active_user(user) -> User` — проверяет is_active
- `get_premium_user(user) -> User` — проверяет subscription_status == 'premium'
- `get_admin_user(user) -> User` — проверяет is_admin

### 2.7 Pydantic Schemas (backend/app/schemas/)

**places.py:**
```python
class AccessibilityBase(BaseModel):
    has_step_free_entrance: bool | None
    entrance_door_width_cm: int | None
    has_ramp: bool | None
    has_elevator: bool | None
    elevator_door_width_cm: int | None
    has_accessible_wc: bool | None
    wc_door_width_cm: int | None
    has_accessible_parking: bool | None
    parking_distance_m: int | None
    floor_surface: str | None
    extra_notes: str | None

class PlaceBase(BaseModel):
    name: str
    description: str | None
    category: Literal["hotel","restaurant","attraction","transport","service"]
    address: str
    city: str = "Москва"
    latitude: Decimal
    longitude: Decimal
    entrance_lat: Decimal | None
    entrance_lng: Decimal | None
    parking_lat: Decimal | None
    parking_lng: Decimal | None
    price_level: int | None = Field(None, ge=1, le=3)
    is_free_entry: bool = False
    working_hours: dict | None
    phone: str | None
    website_url: str | None

class PlaceCreate(PlaceBase):
    accessibility: AccessibilityBase | None
    is_free: bool = False

class PlaceUpdate(PlaceBase):
    accessibility: AccessibilityBase | None

class PlaceResponse(PlaceBase):
    id: UUID
    slug: str
    is_verified: bool
    verified_at: datetime | None
    is_free: bool
    is_published: bool
    media: list[MediaResponse] = []
    accessibility: AccessibilityBase | None
    avg_rating: float | None
    review_count: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PlaceListResponse(BaseModel):
    items: list[PlaceResponse]
    total: int
    page: int
    limit: int
    pages: int
```

**routes.py, reviews.py, users.py, billing.py** — создай по аналогии.

### 2.8 API Эндпоинты

#### backend/app/api/v1/auth.py

Реализуй **полностью** следующие эндпоинты:

**POST /auth/register**
- Body: `{ email, password (min 8), full_name }`
- Проверяет уникальность email
- Создаёт пользователя с хешированным паролем
- Отправляет письмо верификации (ссылка с JWT-токеном на 24 часа)
- Возвращает: `{ message: "Письмо с подтверждением отправлено на {email}" }`

**POST /auth/login**
- Body: `{ email, password }`
- Проверяет credentials
- Возвращает access_token + refresh_token в httpOnly cookies
- Тело ответа: `{ user: UserResponse }`

**POST /auth/refresh**
- Читает refresh_token из cookie
- Выдаёт новый access_token
- Ротирует refresh_token

**POST /auth/logout**
- Инвалидирует refresh_token (записывает в Redis blacklist)
- Очищает cookies

**GET /auth/verify-email/{token}**
- Декодирует JWT-токен верификации
- Устанавливает is_verified = True
- Редиректит на /login?verified=true

**POST /auth/forgot-password**
- Отправляет письмо со ссылкой сброса пароля (токен 1 час)
- Всегда возвращает 200 (не раскрывать существование email)

**POST /auth/reset-password**
- Body: `{ token, new_password }`
- Обновляет пароль

#### backend/app/api/v1/places.py

**GET /places** — с пагинацией и фильтрами:
```python
@router.get("/", response_model=PlaceListResponse)
async def get_places(
    category: str | None = None,
    city: str | None = None,
    has_elevator: bool | None = None,
    has_step_free_entrance: bool | None = None,
    has_accessible_wc: bool | None = None,
    has_accessible_parking: bool | None = None,
    min_door_width: int | None = None,
    price_level: str | None = None,  # "1,2" → [1, 2]
    is_verified: bool | None = None,
    search: str | None = None,
    page: int = 1,
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
```

Логика доступа:
- Анонимный / free пользователь: только места с `is_free=True` и `is_published=True`
- Premium пользователь: все опубликованные места

Соединяй `places` с `place_accessibility` через LEFT JOIN для фильтрации по параметрам доступности.

**GET /places/{id}** — полная карточка места с accessibility, media и средним рейтингом.

**POST /places**, **PUT /places/{id}**, **DELETE /places/{id}** — только для admin.

**POST /places/{id}/save** и **DELETE /places/{id}/save** — добавить/убрать из избранного.

#### backend/app/api/v1/routes.py

**GET /routes/construct** — ключевой эндпоинт конструктора:
```python
@router.get("/construct", response_model=list[RouteConstructResponse])
async def construct_route(
    duration_days: int = Query(1, ge=1, le=2),
    tags: str | None = None,           # "гастро,культура"
    has_elevator: bool | None = None,
    has_accessible_wc: bool | None = None,
    min_door_width: int | None = None,
    city: str = "Москва",
    current_user: User = Depends(get_premium_user),
    db: AsyncSession = Depends(get_db),
):
```

Алгоритм подбора:
1. Найти все опубликованные верифицированные места по параметрам доступности пользователя
2. Если переданы теги — фильтровать маршруты по тегам
3. Если есть готовые редакционные маршруты (is_editorial=True) по параметрам — вернуть их первыми
4. Иначе — создать новый маршрут: подобрать 3–5 мест на день (по городу, разные категории)
5. Рассчитать примерное расстояние между точками

**GET /routes/{id}/export-pdf** — генерировать PDF через reportlab или weasyprint с:
- Названием и описанием маршрута
- Списком мест с адресами и параметрами доступности
- QR-кодом на страницу маршрута
- Датой экспорта

#### backend/app/api/v1/reviews.py

**POST /reviews** — создать отзыв:
- Поле `entity_type`: только "place" или "route"
- Поле `entity_id`: проверить существование объекта
- Фото до 5 штук — загружать на S3 через storage_service
- Status по умолчанию: "pending" (на модерацию)

**PATCH /reviews/{id}/moderate** — только admin:
- Body: `{ status: "approved" | "rejected", note?: str }`
- После одобрения отправить email пользователю

#### backend/app/api/v1/billing.py

**POST /billing/subscribe**:
1. Принять body: `{ plan: "monthly" | "annual" }`
2. Создать платёж через ЮKassa API:
```python
import httpx
async def create_yukassa_payment(amount: str, description: str, return_url: str, idempotency_key: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.yookassa.ru/v3/payments",
            auth=(settings.YUKASSA_SHOP_ID, settings.YUKASSA_SECRET_KEY),
            headers={"Idempotence-Key": idempotency_key},
            json={
                "amount": {"value": amount, "currency": "RUB"},
                "description": description,
                "confirmation": {
                    "type": "redirect",
                    "return_url": return_url
                },
                "capture": True
            }
        )
        return response.json()
```
3. Сохранить черновик подписки в БД со статусом 'pending'
4. Вернуть `{ payment_url: str }`

**POST /billing/webhook** — обработчик вебхука от ЮKassa:
1. Проверить IP-адрес (только доверенные IP ЮKassa)
2. При `event = "payment.succeeded"`: обновить подписку на 'active', обновить subscription_status пользователя
3. При `event = "payment.canceled"`: удалить pending-подписку

### 2.9 backend/app/services/storage_service.py

```python
import boto3
from botocore.config import Config
from app.core.config import settings
import uuid

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    endpoint_url=settings.S3_ENDPOINT,
    region_name=settings.S3_REGION,
    config=Config(signature_version="s3v4")
)

async def upload_file(file_bytes: bytes, content_type: str, folder: str = "media") -> str:
    """Загружает файл в S3 и возвращает публичный URL."""
    file_key = f"{folder}/{uuid.uuid4()}"
    s3_client.put_object(
        Bucket=settings.S3_BUCKET,
        Key=file_key,
        Body=file_bytes,
        ContentType=content_type,
        ACL="public-read"
    )
    return f"{settings.S3_ENDPOINT}/{settings.S3_BUCKET}/{file_key}"
```

Максимальный размер файла: 10 MB. Разрешённые типы: image/jpeg, image/png, image/webp.

### 2.10 backend/app/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, places, routes, reviews, users, billing, admin

app = FastAPI(
    title="Колесим самостоятельно API",
    version="1.0.0",
    docs_url="/api/docs" if settings.ENVIRONMENT == "development" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(places.router, prefix="/api/v1/places", tags=["places"])
app.include_router(routes.router, prefix="/api/v1/routes", tags=["routes"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(billing.router, prefix="/api/v1/billing", tags=["billing"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
```

### 2.11 Alembic

Настрой Alembic для async PostgreSQL:
- `alembic/env.py` — используй `run_async_migrations()` с `AsyncEngine`
- Создай первую миграцию `alembic revision --autogenerate -m "initial"`

### 2.12 backend/Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

## ЗАДАЧА 3: FRONTEND

### 3.1 Инициализация

Создай Next.js 14 проект с App Router, TypeScript, Tailwind CSS.

`frontend/package.json` dependencies:
```json
{
  "dependencies": {
    "next": "14.2.5",
    "react": "^18",
    "react-dom": "^18",
    "typescript": "^5",
    "@tanstack/react-query": "^5",
    "zustand": "^4",
    "axios": "^1.7",
    "react-hook-form": "^7",
    "zod": "^3",
    "@hookform/resolvers": "^3",
    "leaflet": "^1.9",
    "react-leaflet": "^4",
    "@types/leaflet": "^1.9",
    "lucide-react": "^0.400",
    "class-variance-authority": "^0.7",
    "clsx": "^2",
    "tailwind-merge": "^2",
    "@radix-ui/react-dialog": "^1",
    "@radix-ui/react-select": "^2",
    "@radix-ui/react-checkbox": "^1",
    "@radix-ui/react-toast": "^1",
    "@radix-ui/react-tabs": "^1"
  }
}
```

### 3.2 frontend/src/lib/api.ts

Создай axios instance с interceptors:
```typescript
import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
  withCredentials: true, // для httpOnly cookies
});

// Interceptor: при 401 → попытка refresh → повтор запроса
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      await api.post("/auth/refresh");
      return api(error.config);
    }
    return Promise.reject(error);
  }
);

export default api;
```

Экспортируй типизированные функции для каждого эндпоинта.

### 3.3 frontend/src/types/

Создай TypeScript типы, зеркалящие Pydantic схемы:

```typescript
// place.ts
export interface Accessibility {
  has_step_free_entrance: boolean | null;
  entrance_door_width_cm: number | null;
  has_ramp: boolean | null;
  has_elevator: boolean | null;
  elevator_door_width_cm: number | null;
  has_accessible_wc: boolean | null;
  wc_door_width_cm: number | null;
  has_accessible_parking: boolean | null;
  parking_distance_m: number | null;
  floor_surface: string | null;
  extra_notes: string | null;
}

export interface Place {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  category: "hotel" | "restaurant" | "attraction" | "transport" | "service";
  address: string;
  city: string;
  latitude: number;
  longitude: number;
  entrance_lat: number | null;
  entrance_lng: number | null;
  parking_lat: number | null;
  parking_lng: number | null;
  price_level: 1 | 2 | 3 | null;
  is_verified: boolean;
  verified_at: string | null;
  is_free: boolean;
  is_published: boolean;
  media: Media[];
  accessibility: Accessibility | null;
  avg_rating: number | null;
  review_count: number;
  created_at: string;
}

export interface PlaceListResponse {
  items: Place[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}
```

### 3.4 Страницы

#### app/(public)/page.tsx — Главная (лендинг)

Разделы лендинга:
1. **Hero** — заголовок «Путешествуй на коляске. Без сюрпризов.», подзаголовок, CTA «Смотреть маршруты» и «Начать бесплатно»
2. **Проблема** — блок с 3 иконками: «Ложная доступность», «Дни на проверку», «Риск разочарования»
3. **Решение** — что проверяет команда (фото входа, замеры, GPS)
4. **Тарифы** — freemium + premium с кнопкой оплаты
5. **Отзывы** — 3 цитаты от пользователей
6. **Footer** — ссылки, email

Стиль: чистый, профессиональный. Основной цвет: синий (#2563EB). Акцент: зелёный (#16A34A). Нейтральные: серые тона. Крупный читаемый шрифт (font-size min 16px для основного текста).

#### app/(public)/catalog/page.tsx — Каталог объектов

- Сайдбар с фильтрами (PlaceFilters) слева
- Сетка карточек (PlaceCard) справа (2 колонки на десктопе, 1 на мобиле)
- Пагинация
- Для premium-контента — PaywallModal при клике

#### app/(public)/catalog/[id]/page.tsx — Карточка объекта

- Галерея фото (первое фото — большое, остальные сетка)
- Бейдж «Проверено» с датой
- Таблица параметров доступности (иконки: ✅ / ❌ / ⚠️)
- Карта Leaflet с пином входа и парковки
- Кнопка «Добавить в избранное»
- Отзывы пользователей
- Форма отзыва (для авторизованных)

Используй SSG: `generateStaticParams` + `generateMetadata` для SEO.

#### app/(public)/routes/page.tsx — Каталог маршрутов

- Карточки маршрутов (RouteCard) с тегами, длительностью, сложностью
- Фильтр: по длительности (1 день / 2 дня), по тегам
- Paywall для premium-маршрутов

#### app/(protected)/constructor/page.tsx — Конструктор маршрута

Пошаговая форма (wizard):
1. Шаг 1: «Сколько дней?» — 1 или 2
2. Шаг 2: «Что интересует?» — мультивыбор тегов (природа, культура, гастро, шопинг)
3. Шаг 3: «Параметры доступности» — чекбоксы (лифт, пандус, санузел, парковка), мин. ширина двери
4. Шаг 4: Результат — карта + список мест, можно поменять местами (drag & drop), добавить/убрать
5. Кнопки: «Сохранить маршрут» + «Экспорт PDF»

#### app/(protected)/billing/page.tsx — Страница подписки

- Текущий тариф и дата истечения (если premium)
- Карточки тарифов (Тариф «Месяц» и «Год» с экономией)
- Кнопка «Оформить» → POST /billing/subscribe → redirect на payment_url
- История платежей

#### admin/ — Административная панель

Простой, функциональный интерфейс (не нужно красивое — нужно рабочее):
- Таблицы с сортировкой и поиском
- Кнопки действий: верифицировать, опубликовать, удалить
- Форма добавления/редактирования объекта с полями доступности
- Очередь модерации отзывов

### 3.5 Ключевые компоненты

**components/catalog/AccessibilityBadge.tsx**

Компонент отображения параметра доступности:
```tsx
interface AccessibilityBadgeProps {
  label: string;
  value: boolean | null;
  detail?: string; // напр. "85 см"
}
// true → зелёная иконка ✅
// false → красная ❌
// null → серая ⚠️ "Нет данных"
```

**components/catalog/PlaceFilters.tsx**

Фильтры с URL-синхронизацией (используй `useSearchParams` + `useRouter`):
- Категория: Radio group
- Параметры доступности: Checkbox группа
- Мин. ширина двери: Number input
- Ценовой уровень: Toggle (₽ / ₽₽ / ₽₽₽)
- «Только проверенные»: Switch
- Кнопка «Сбросить фильтры»

**components/catalog/PlaceMap.tsx**

Leaflet карта с двумя слоями:
```tsx
// Пин входа — синий маркер
// Пин парковки — зелёный маркер P
// Используй dynamic import с ssr: false (Leaflet не работает на сервере)
const MapComponent = dynamic(() => import("./MapInner"), { ssr: false });
```

**components/billing/PaywallModal.tsx**

Модальное окно при попытке просмотреть premium-контент:
- Заголовок: «Это доступно в Premium»
- Список того, что открывается
- CTA: «Оформить за 299 ₽/мес» → /billing
- Ссылка «Продолжить бесплатно» — закрыть модал

### 3.6 Хуки (hooks/)

**useAuth.ts** — Zustand store:
```typescript
interface AuthStore {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  fetchMe: () => Promise<void>;
  isPremium: () => boolean;
  isAdmin: () => boolean;
}
```

**usePlaces.ts** — React Query:
```typescript
export function usePlaces(filters: PlaceFilters) {
  return useQuery({
    queryKey: ["places", filters],
    queryFn: () => placesApi.getPlaces(filters),
    staleTime: 5 * 60 * 1000, // 5 мин кэш
  });
}

export function usePlace(id: string) {
  return useQuery({
    queryKey: ["places", id],
    queryFn: () => placesApi.getPlace(id),
    staleTime: 10 * 60 * 1000,
  });
}
```

### 3.7 Middleware для protected роутов (middleware.ts)

```typescript
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PROTECTED_PATHS = ["/constructor", "/profile", "/my-routes", "/favorites", "/billing"];
const ADMIN_PATHS = ["/admin"];

export function middleware(request: NextRequest) {
  const token = request.cookies.get("access_token");
  const { pathname } = request.nextUrl;

  if (PROTECTED_PATHS.some(p => pathname.startsWith(p)) && !token) {
    return NextResponse.redirect(new URL(`/login?next=${pathname}`, request.url));
  }
  
  return NextResponse.next();
}
```

### 3.8 frontend/Dockerfile

```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
```

---

## ЗАДАЧА 4: ТЕСТЫ

### 4.1 backend/tests/conftest.py

```python
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.core.database import Base, get_db

TEST_DATABASE_URL = "postgresql+asyncpg://kolesim_user:changeme@localhost:5432/kolesim_test"

@pytest_asyncio.fixture
async def db():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client(db):
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
```

Напиши тесты для:
- `test_auth.py`: регистрация, логин, неверный пароль, refresh token
- `test_places.py`: получение списка (anon видит только free), фильтры по доступности, карточка
- `test_billing.py`: создание платежа, обработка webhook

---

## ЗАДАЧА 5: ПОРЯДОК ВЫПОЛНЕНИЯ

Выполняй задачи строго в этом порядке:

1. `docker-compose.yml`, `.env.example`, `nginx.conf` — базовая инфраструктура
2. `backend/` — models → core/config, security, database → schemas → services → api → main → alembic
3. Запусти `docker compose up db` и проверь подключение
4. `alembic upgrade head` — создай таблицы
5. `frontend/` — types → lib/api → hooks → components → pages → middleware
6. Полный `docker compose up` — убедись, что всё запускается
7. Тесты

**После каждой задачи** выводи краткую сводку: что создано, что осталось.

---

## ЗАДАЧА 6: SEED DATA (стартовые данные)

Создай `backend/scripts/seed.py` — скрипт для заполнения БД тестовыми данными:

```python
# Создаёт:
# 1. Администратора: admin@kolesim.ru / Admin12345!
# 2. Тестового пользователя: test@kolesim.ru / Test12345! (free)
# 3. Premium пользователя: premium@kolesim.ru / Premium12345!
# 4. 15 объектов в Москве с разными параметрами доступности:
#    - 5 ресторанов (3 с лифтом, все с пандусом, разная ширина дверей)
#    - 4 достопримечательности (Третьяковка, Парк Горького, Коломенское, ГУМ)
#    - 3 отеля
#    - 2 транспортных узла
#    - 1 сервис (медицинский центр)
# 5. 3 готовых редакционных маршрута (is_editorial=True)
# 6. 10 отзывов (moderation_status='approved')
#
# Все реальные объекты — с реальными GPS-координатами Москвы.
# Помечай 5 объектов как is_free=True (freemium-доступ).
```

---

## КРИТЕРИИ ГОТОВНОСТИ MVP

✅ `docker compose up` — все 5 контейнеров запускаются без ошибок  
✅ `GET /api/health` → `{"status": "ok"}`  
✅ Регистрация → логин → просмотр каталога (freemium) без ошибок  
✅ Оформление подписки → webhook → статус premium обновился  
✅ Конструктор маршрута возвращает минимум 2 места  
✅ Карта отображает пины входа и парковки  
✅ PDF-экспорт маршрута скачивается  
✅ Все тесты проходят: `pytest tests/ -v`  
✅ Lighthouse accessibility score ≥ 85  
✅ Нет console.error в браузере при стандартных сценариях  

---

*Промпт версии 1.0 — платформа «Колесим самостоятельно»*
