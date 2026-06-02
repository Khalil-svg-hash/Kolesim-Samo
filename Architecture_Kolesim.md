# Архитектура и технический стек: «Колесим самостоятельно»
> MVP — Web-платформа для маломобильных туристов

**Версия:** 1.0  
**Дата:** Июнь 2025

---

## 1. Обзор архитектуры

```
┌─────────────────────────────────────────────────────────┐
│                        КЛИЕНТ                           │
│          Next.js (SSR/SSG) + TypeScript                 │
│          React Query  │  Leaflet Maps  │  Tailwind CSS  │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTPS / REST API
┌───────────────────────▼─────────────────────────────────┐
│                  NGINX (reverse proxy)                  │
│              SSL termination, rate limiting             │
└──────────┬──────────────────────────┬───────────────────┘
           │                          │
┌──────────▼──────────┐   ┌──────────▼──────────────────┐
│  FastAPI (Python)   │   │    Static files / Media      │
│  REST API v1        │   │    S3 / Yandex Object Storage│
│  JWT Auth           │   └─────────────────────────────-┘
│  Pydantic schemas   │
└──────────┬──────────┘
           │
┌──────────▼──────────────────────────────────────────────┐
│                   PostgreSQL 15                         │
│              Основная база данных                       │
└─────────────────────────────────────────────────────────┘
           │
┌──────────▼──────────┐   ┌──────────────────────────────┐
│   Redis (Cache)     │   │    ЮKassa (Payments)         │
│   Сессии, TTL кэш  │   │    Webhook → FastAPI         │
└─────────────────────┘   └──────────────────────────────┘
```

**Паттерн:** Monolith-first MVP. Единый FastAPI-сервис, единая БД. Горизонтальное масштабирование при необходимости — позднее.

---

## 2. Технологический стек

### 2.1 Backend

| Компонент | Технология | Версия | Обоснование |
|---|---|---|---|
| Язык | Python | 3.12+ | Команда знает, богатая экосистема |
| Web-фреймворк | FastAPI | 0.111+ | Async, автодокументация OpenAPI, скорость |
| ORM | SQLAlchemy | 2.0+ | Async ORM, типобезопасность |
| Миграции | Alembic | 1.13+ | Стандарт для SQLAlchemy |
| Валидация | Pydantic | 2.x | Встроен в FastAPI |
| Авторизация | python-jose + passlib | — | JWT + bcrypt |
| Email | FastAPI-Mail | — | Верификация, уведомления |
| S3-клиент | boto3 | — | Загрузка медиафайлов |
| HTTP-клиент | httpx | — | Запросы к внешним API (ЮKassa) |
| Тесты | pytest + httpx | — | Unit + integration тесты |

### 2.2 Frontend

| Компонент | Технология | Версия | Обоснование |
|---|---|---|---|
| Язык | TypeScript | 5.x | Типобезопасность |
| Фреймворк | Next.js (App Router) | 14.x | SSR/SSG для SEO, file-based routing |
| UI | Tailwind CSS | 3.x | Скорость разработки, консистентность |
| Компоненты | shadcn/ui | — | Accessible-компоненты из коробки |
| Состояние сервера | React Query (TanStack) | 5.x | Кэш, загрузка, мутации |
| Глобальное состояние | Zustand | 4.x | Простота, минимализм |
| Карты | Leaflet + React-Leaflet | — | OSM, бесплатно, без API-ключа |
| Иконки | Lucide React | — | Accessibility-friendly |
| Формы | React Hook Form + Zod | — | Валидация на клиенте |
| PDF-экспорт | @react-pdf/renderer | — | Клиентский PDF |

### 2.3 База данных

| Компонент | Технология | Обоснование |
|---|---|---|
| Основная БД | PostgreSQL 15 | JSONB, GIS-расширения, надёжность |
| Расширение | PostGIS (опционально) | Геопоиск по радиусу (v1.1) |
| Кэш | Redis 7 | Кэш каталога, rate limiting |
| Хранение файлов | Yandex Object Storage (S3) | Российский провайдер, S3-совместимый |

### 2.4 Инфраструктура

| Компонент | Технология | Обоснование |
|---|---|---|
| Контейнеризация | Docker + Docker Compose | Стандарт, воспроизводимость |
| Reverse proxy | Nginx | SSL, rate limit, gzip |
| SSL | Let's Encrypt / Certbot | Бесплатно |
| CI/CD | GitHub Actions | Автодеплой на VPS |
| Хостинг | VPS (Yandex Cloud / Selectel) | Российские датацентры |
| Мониторинг | Posthog (product) + Sentry (errors) | SaaS-решения |
| Аналитика | Yandex Metrika | Основная аудитория — РФ |

---

## 3. Структура проекта (Monorepo)

```
kolesim/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py          # регистрация, логин, токены
│   │   │       ├── places.py        # CRUD объектов, фильтры
│   │   │       ├── routes.py        # CRUD маршрутов, конструктор
│   │   │       ├── reviews.py       # отзывы, модерация
│   │   │       ├── users.py         # профиль, избранное
│   │   │       ├── billing.py       # подписка, вебхуки ЮKassa
│   │   │       └── admin.py         # административные эндпоинты
│   │   ├── core/
│   │   │   ├── config.py            # pydantic settings, env
│   │   │   ├── security.py          # JWT, bcrypt
│   │   │   ├── database.py          # async engine, sessions
│   │   │   └── dependencies.py      # DI: get_db, get_current_user
│   │   ├── models/                  # SQLAlchemy ORM models
│   │   │   ├── user.py
│   │   │   ├── place.py
│   │   │   ├── place_accessibility.py
│   │   │   ├── route.py
│   │   │   ├── review.py
│   │   │   ├── media.py
│   │   │   └── subscription.py
│   │   ├── schemas/                 # Pydantic schemas (request/response)
│   │   │   ├── user.py
│   │   │   ├── place.py
│   │   │   ├── route.py
│   │   │   ├── review.py
│   │   │   └── billing.py
│   │   ├── services/                # бизнес-логика
│   │   │   ├── auth_service.py
│   │   │   ├── place_service.py
│   │   │   ├── route_service.py
│   │   │   ├── review_service.py
│   │   │   ├── billing_service.py
│   │   │   └── storage_service.py   # S3 upload
│   │   ├── utils/
│   │   │   ├── email.py
│   │   │   └── pagination.py
│   │   └── main.py                  # FastAPI app factory
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_places.py
│   │   ├── test_routes.py
│   │   └── test_auth.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/                     # Next.js App Router
│   │   │   ├── (public)/
│   │   │   │   ├── page.tsx         # Главная (лендинг)
│   │   │   │   ├── catalog/
│   │   │   │   │   ├── page.tsx     # Каталог объектов
│   │   │   │   │   └── [id]/
│   │   │   │   │       └── page.tsx # Карточка объекта
│   │   │   │   └── routes/
│   │   │   │       ├── page.tsx     # Каталог маршрутов
│   │   │   │       └── [id]/
│   │   │   │           └── page.tsx # Карточка маршрута
│   │   │   ├── (auth)/
│   │   │   │   ├── login/page.tsx
│   │   │   │   ├── register/page.tsx
│   │   │   │   └── forgot-password/page.tsx
│   │   │   ├── (protected)/
│   │   │   │   ├── profile/page.tsx
│   │   │   │   ├── constructor/page.tsx  # Конструктор маршрута
│   │   │   │   ├── my-routes/page.tsx
│   │   │   │   ├── favorites/page.tsx
│   │   │   │   └── billing/page.tsx
│   │   │   ├── admin/               # Административная панель
│   │   │   │   ├── places/page.tsx
│   │   │   │   ├── routes/page.tsx
│   │   │   │   ├── reviews/page.tsx
│   │   │   │   └── users/page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   ├── ui/                  # shadcn/ui переопределения
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   └── MobileNav.tsx
│   │   │   ├── catalog/
│   │   │   │   ├── PlaceCard.tsx
│   │   │   │   ├── PlaceFilters.tsx
│   │   │   │   ├── AccessibilityBadge.tsx
│   │   │   │   └── PlaceMap.tsx
│   │   │   ├── routes/
│   │   │   │   ├── RouteCard.tsx
│   │   │   │   └── RouteMap.tsx
│   │   │   ├── constructor/
│   │   │   │   ├── ConstructorForm.tsx
│   │   │   │   ├── PlacePicker.tsx
│   │   │   │   └── RoutePreview.tsx
│   │   │   ├── reviews/
│   │   │   │   ├── ReviewCard.tsx
│   │   │   │   └── ReviewForm.tsx
│   │   │   └── billing/
│   │   │       ├── PricingCard.tsx
│   │   │       └── PaywallModal.tsx
│   │   ├── lib/
│   │   │   ├── api.ts               # axios instance + endpoints
│   │   │   ├── auth.ts              # auth helpers
│   │   │   └── utils.ts
│   │   ├── hooks/
│   │   │   ├── usePlaces.ts
│   │   │   ├── useRoutes.ts
│   │   │   └── useAuth.ts
│   │   └── types/
│   │       ├── place.ts
│   │       ├── route.ts
│   │       └── user.ts
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   └── next.config.js
│
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
├── docker-compose.prod.yml
└── .env.example
```

---

## 4. Схема базы данных

### Ключевые таблицы

```sql
-- =====================
-- ПОЛЬЗОВАТЕЛИ
-- =====================
CREATE TABLE users (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email                 VARCHAR(255) UNIQUE NOT NULL,
    hashed_password       VARCHAR(255) NOT NULL,
    full_name             VARCHAR(255),
    avatar_url            TEXT,
    wheelchair_type       VARCHAR(50),          -- manual | electric | child | unknown
    min_door_width_cm     INT DEFAULT 60,        -- персональный фильтр
    needs_accessible_wc   BOOLEAN DEFAULT false,
    is_active             BOOLEAN DEFAULT true,
    is_verified           BOOLEAN DEFAULT false,
    is_admin              BOOLEAN DEFAULT false,
    subscription_status   VARCHAR(50) DEFAULT 'free',   -- free | premium
    subscription_expires_at TIMESTAMP WITH TIME ZONE,
    created_at            TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at            TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================
-- ОБЪЕКТЫ (МЕСТА)
-- =====================
CREATE TABLE places (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                  VARCHAR(255) NOT NULL,
    slug                  VARCHAR(255) UNIQUE NOT NULL,  -- для SEO URL
    description           TEXT,
    category              VARCHAR(100) NOT NULL,         -- hotel | restaurant | attraction | transport | service
    address               TEXT NOT NULL,
    city                  VARCHAR(100) DEFAULT 'Москва',
    latitude              DECIMAL(10, 8) NOT NULL,
    longitude             DECIMAL(11, 8) NOT NULL,
    entrance_lat          DECIMAL(10, 8),               -- GPS входа (отдельно!)
    entrance_lng          DECIMAL(11, 8),
    parking_lat           DECIMAL(10, 8),               -- GPS парковки
    parking_lng           DECIMAL(11, 8),
    price_level           SMALLINT CHECK (price_level BETWEEN 1 AND 3),  -- 1=₽ 2=₽₽ 3=₽₽₽
    is_free_entry         BOOLEAN DEFAULT false,         -- бесплатный вход
    working_hours         JSONB,                         -- {"mon": "10:00-22:00", ...}
    phone                 VARCHAR(50),
    website_url           TEXT,
    is_verified           BOOLEAN DEFAULT false,
    verified_at           TIMESTAMP WITH TIME ZONE,
    verified_by           UUID REFERENCES users(id),
    is_free               BOOLEAN DEFAULT false,         -- freemium: видно без подписки
    is_published          BOOLEAN DEFAULT false,
    created_by            UUID REFERENCES users(id),
    created_at            TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at            TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================
-- ДОСТУПНОСТЬ ОБЪЕКТА
-- =====================
CREATE TABLE place_accessibility (
    id                        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    place_id                  UUID REFERENCES places(id) ON DELETE CASCADE UNIQUE,
    has_step_free_entrance    BOOLEAN,
    entrance_door_width_cm    INT,
    has_ramp                  BOOLEAN,
    ramp_angle_deg            DECIMAL(4,1),
    has_elevator              BOOLEAN,
    elevator_door_width_cm    INT,
    elevator_notes            TEXT,
    has_accessible_wc         BOOLEAN,
    wc_door_width_cm          INT,
    wc_notes                  TEXT,
    has_accessible_parking    BOOLEAN,
    parking_distance_m        INT,
    floor_surface             VARCHAR(100),   -- asphalt | tile | gravel | cobblestone | mixed
    extra_notes               TEXT,
    last_checked_at           TIMESTAMP WITH TIME ZONE,
    checked_by                UUID REFERENCES users(id),
    created_at                TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at                TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================
-- МЕДИАФАЙЛЫ
-- =====================
CREATE TABLE media (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type     VARCHAR(50) NOT NULL,  -- place | route | review
    entity_id       UUID NOT NULL,
    url             TEXT NOT NULL,
    thumbnail_url   TEXT,
    caption         TEXT,
    media_type      VARCHAR(50) DEFAULT 'photo',  -- photo | video
    sort_order      INT DEFAULT 0,
    uploaded_by     UUID REFERENCES users(id),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================
-- МАРШРУТЫ
-- =====================
CREATE TABLE routes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title           VARCHAR(255) NOT NULL,
    slug            VARCHAR(255) UNIQUE NOT NULL,
    description     TEXT,
    duration_days   SMALLINT DEFAULT 1 CHECK (duration_days BETWEEN 1 AND 2),
    distance_km     DECIMAL(6, 2),
    difficulty      VARCHAR(50),            -- easy | medium | hard
    tags            TEXT[],                 -- ['природа', 'гастро', 'культура']
    is_editorial    BOOLEAN DEFAULT false,  -- маршрут от команды
    is_published    BOOLEAN DEFAULT false,
    is_free         BOOLEAN DEFAULT false,
    view_count      INT DEFAULT 0,
    created_by      UUID REFERENCES users(id),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================
-- МЕСТА В МАРШРУТЕ (M2M)
-- =====================
CREATE TABLE route_places (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    route_id                UUID REFERENCES routes(id) ON DELETE CASCADE,
    place_id                UUID REFERENCES places(id),
    order_index             INT NOT NULL,
    day_number              SMALLINT DEFAULT 1,
    notes                   TEXT,
    estimated_duration_min  INT,
    UNIQUE (route_id, order_index)
);

-- =====================
-- ОТЗЫВЫ
-- =====================
CREATE TABLE reviews (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID REFERENCES users(id),
    entity_type             VARCHAR(50) NOT NULL,    -- place | route
    entity_id               UUID NOT NULL,
    rating                  SMALLINT CHECK (rating BETWEEN 1 AND 5),
    accessibility_rating    SMALLINT CHECK (accessibility_rating BETWEEN 1 AND 5),
    text                    TEXT,
    visited_at              DATE,
    wheelchair_type         VARCHAR(50),
    moderation_status       VARCHAR(50) DEFAULT 'pending',  -- pending | approved | rejected
    moderation_note         TEXT,
    moderated_by            UUID REFERENCES users(id),
    moderated_at            TIMESTAMP WITH TIME ZONE,
    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================
-- ИЗБРАННОЕ
-- =====================
CREATE TABLE user_saved_places (
    user_id    UUID REFERENCES users(id) ON DELETE CASCADE,
    place_id   UUID REFERENCES places(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, place_id)
);

CREATE TABLE user_saved_routes (
    user_id    UUID REFERENCES users(id) ON DELETE CASCADE,
    route_id   UUID REFERENCES routes(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, route_id)
);

-- =====================
-- ПОДПИСКИ
-- =====================
CREATE TABLE subscriptions (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID REFERENCES users(id),
    plan                    VARCHAR(50) NOT NULL,        -- monthly | annual
    status                  VARCHAR(50) NOT NULL,        -- active | cancelled | expired
    payment_provider        VARCHAR(50) DEFAULT 'yukassa',
    provider_payment_id     VARCHAR(255),
    amount_rub              DECIMAL(10, 2),
    started_at              TIMESTAMP WITH TIME ZONE NOT NULL,
    expires_at              TIMESTAMP WITH TIME ZONE NOT NULL,
    cancelled_at            TIMESTAMP WITH TIME ZONE,
    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================
-- ИНДЕКСЫ
-- =====================
CREATE INDEX idx_places_category ON places(category);
CREATE INDEX idx_places_city ON places(city);
CREATE INDEX idx_places_is_published ON places(is_published);
CREATE INDEX idx_places_is_verified ON places(is_verified);
CREATE INDEX idx_places_coords ON places(latitude, longitude);
CREATE INDEX idx_reviews_entity ON reviews(entity_type, entity_id);
CREATE INDEX idx_media_entity ON media(entity_type, entity_id);
CREATE INDEX idx_route_places_route ON route_places(route_id);
```

---

## 5. API — Эндпоинты

### 5.1 Аутентификация (`/api/v1/auth`)

| Метод | URL | Описание | Auth |
|---|---|---|---|
| POST | `/auth/register` | Регистрация по email | — |
| POST | `/auth/login` | Логин, получение JWT | — |
| POST | `/auth/refresh` | Обновление access token | refresh token |
| POST | `/auth/logout` | Инвалидация refresh token | ✓ |
| POST | `/auth/forgot-password` | Запрос сброса пароля | — |
| POST | `/auth/reset-password` | Сброс пароля по токену | — |
| GET | `/auth/verify-email/{token}` | Верификация email | — |

### 5.2 Объекты (`/api/v1/places`)

| Метод | URL | Описание | Auth |
|---|---|---|---|
| GET | `/places` | Список с фильтрами и пагинацией | partial |
| GET | `/places/{id}` | Карточка объекта | partial |
| GET | `/places/{id}/accessibility` | Параметры доступности | ✓ premium |
| GET | `/places/{id}/reviews` | Отзывы объекта | ✓ premium |
| GET | `/places/{id}/media` | Медиафайлы | partial |
| POST | `/places` | Создать объект | ✓ admin |
| PUT | `/places/{id}` | Обновить объект | ✓ admin |
| DELETE | `/places/{id}` | Удалить объект | ✓ admin |
| POST | `/places/{id}/save` | Добавить в избранное | ✓ |
| DELETE | `/places/{id}/save` | Убрать из избранного | ✓ |

Query params для GET /places:
```
?category=restaurant
&city=Москва
&has_elevator=true
&has_step_free_entrance=true
&has_accessible_wc=true
&min_door_width=80
&price_level=1,2
&is_verified=true
&is_free=true
&search=кафе
&page=1
&limit=20
&sort=rating|-created_at
```

### 5.3 Маршруты (`/api/v1/routes`)

| Метод | URL | Описание | Auth |
|---|---|---|---|
| GET | `/routes` | Список маршрутов | partial |
| GET | `/routes/{id}` | Карточка маршрута | ✓ premium |
| POST | `/routes` | Создать маршрут | ✓ |
| PUT | `/routes/{id}` | Обновить маршрут | ✓ owner/admin |
| DELETE | `/routes/{id}` | Удалить маршрут | ✓ owner/admin |
| POST | `/routes/{id}/save` | В избранное | ✓ |
| GET | `/routes/construct` | Автоподбор маршрута | ✓ premium |
| GET | `/routes/{id}/export-pdf` | Генерация PDF | ✓ premium |

Query params для GET /routes/construct:
```
?duration_days=2
&tags=гастро,культура
&has_elevator=true
&city=Москва
```

### 5.4 Отзывы (`/api/v1/reviews`)

| Метод | URL | Описание | Auth |
|---|---|---|---|
| POST | `/reviews` | Создать отзыв | ✓ |
| GET | `/reviews/{id}` | Получить отзыв | — |
| PUT | `/reviews/{id}` | Редактировать отзыв | ✓ owner |
| DELETE | `/reviews/{id}` | Удалить отзыв | ✓ owner/admin |
| PATCH | `/reviews/{id}/moderate` | Модерировать | ✓ admin |

### 5.5 Пользователь (`/api/v1/users`)

| Метод | URL | Описание | Auth |
|---|---|---|---|
| GET | `/users/me` | Профиль текущего пользователя | ✓ |
| PUT | `/users/me` | Обновить профиль | ✓ |
| GET | `/users/me/saved-places` | Избранные места | ✓ |
| GET | `/users/me/saved-routes` | Избранные маршруты | ✓ |
| GET | `/users/me/routes` | Мои маршруты | ✓ |
| POST | `/users/me/avatar` | Загрузить аватар | ✓ |

### 5.6 Биллинг (`/api/v1/billing`)

| Метод | URL | Описание | Auth |
|---|---|---|---|
| GET | `/billing/plans` | Доступные тарифы | — |
| POST | `/billing/subscribe` | Создать платёж ЮKassa | ✓ |
| GET | `/billing/subscription` | Текущая подписка | ✓ |
| POST | `/billing/cancel` | Отменить подписку | ✓ |
| GET | `/billing/history` | История платежей | ✓ |
| POST | `/billing/webhook` | Webhook от ЮKassa | — (secret) |

---

## 6. Авторизация и доступ

### 6.1 Роли
| Роль | Описание |
|---|---|
| `anonymous` | Не авторизован. Видит freemium-контент (is_free=true) |
| `free` | Авторизован, бесплатный тариф. Тот же доступ + профиль + отзывы |
| `premium` | Полный доступ к каталогу и конструктору |
| `admin` | Управление всем контентом |

### 6.2 JWT Flow
```
1. POST /auth/login → { access_token (15 min), refresh_token (30 days) }
2. access_token → httpOnly cookie или Authorization: Bearer
3. POST /auth/refresh → новый access_token
4. POST /auth/logout → инвалидация refresh_token в Redis
```

---

## 7. Docker Compose

```yaml
# docker-compose.yml
version: '3.9'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: kolesim
      POSTGRES_USER: kolesim_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U kolesim_user -d kolesim"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    environment:
      DATABASE_URL: postgresql+asyncpg://kolesim_user:${DB_PASSWORD}@db:5432/kolesim
      REDIS_URL: redis://redis:6379
      SECRET_KEY: ${SECRET_KEY}
      YUKASSA_SHOP_ID: ${YUKASSA_SHOP_ID}
      YUKASSA_SECRET_KEY: ${YUKASSA_SECRET_KEY}
      S3_BUCKET: ${S3_BUCKET}
      S3_ACCESS_KEY: ${S3_ACCESS_KEY}
      S3_SECRET_KEY: ${S3_SECRET_KEY}
      S3_ENDPOINT: https://storage.yandexcloud.net
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    depends_on:
      - backend
    environment:
      NEXT_PUBLIC_API_URL: https://kolesim.ru/api/v1
    ports:
      - "3000:3000"

  nginx:
    image: nginx:alpine
    depends_on:
      - backend
      - frontend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot

volumes:
  postgres_data:
  redis_data:
```

---

## 8. Переменные окружения (.env.example)

```env
# Database
DB_PASSWORD=your_strong_password_here

# JWT
SECRET_KEY=your_256_bit_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30

# Email (SMTP)
SMTP_HOST=smtp.yandex.ru
SMTP_PORT=465
SMTP_USER=noreply@kolesim.ru
SMTP_PASSWORD=your_smtp_password

# ЮKassa
YUKASSA_SHOP_ID=your_shop_id
YUKASSA_SECRET_KEY=your_secret_key
YUKASSA_RETURN_URL=https://kolesim.ru/billing/success

# Yandex Object Storage (S3)
S3_BUCKET=kolesim-media
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key
S3_ENDPOINT=https://storage.yandexcloud.net
S3_REGION=ru-central1

# App
FRONTEND_URL=https://kolesim.ru
BACKEND_URL=https://kolesim.ru/api
ENVIRONMENT=production  # development | production

# Sentry
SENTRY_DSN=your_sentry_dsn

# Redis
REDIS_URL=redis://redis:6379/0
```

---

## 9. CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run backend tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest tests/ -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /opt/kolesim
            git pull origin main
            docker compose -f docker-compose.prod.yml up -d --build
            docker compose exec backend alembic upgrade head
```

---

*Документ подготовлен для команды «Колесим самостоятельно». Версия 1.0 MVP.*
