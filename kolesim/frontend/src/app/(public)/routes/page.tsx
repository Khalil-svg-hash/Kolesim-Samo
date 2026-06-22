"use client";

import { RouteCard } from "@/components/RouteCard";
import type { Route } from "@/types/route";

const MOCK_ROUTES: Route[] = [
  {
    id: "1",
    title: "Доступная Москва",
    slug: "dostupnaya-moskva",
    description: "Маршрут по главным достопримечательностям Москвы с полной доступностью",
    duration_days: 1,
    distance_km: 12,
    difficulty: "easy",
    tags: ["достопримечательности", "музеи"],
    is_editorial: true,
    is_published: true,
    is_free: true,
    view_count: 342,
    created_by: null,
    created_at: "2024-01-01",
    updated_at: "2024-01-01",
    places: [],
  },
  {
    id: "2",
    title: "Санкт-Петербург без барьеров",
    slug: "spb-bez-barerov",
    description: "Двухдневный маршрут по доступным местам Северной столицы",
    duration_days: 2,
    distance_km: 25,
    difficulty: "medium",
    tags: ["культура", "парки"],
    is_editorial: true,
    is_published: true,
    is_free: false,
    view_count: 218,
    created_by: null,
    created_at: "2024-02-01",
    updated_at: "2024-02-01",
    places: [],
  },
  {
    id: "3",
    title: "Казань для всех",
    slug: "kazan-dlya-vseh",
    description: "Однодневный маршрут по Казани с посещением доступных мест",
    duration_days: 1,
    distance_km: 8,
    difficulty: "easy",
    tags: ["история", "гастрономия"],
    is_editorial: false,
    is_published: true,
    is_free: true,
    view_count: 156,
    created_by: "user1",
    created_at: "2024-03-01",
    updated_at: "2024-03-01",
    places: [],
  },
];

export default function RoutesPage() {
  return (
    <div className="bg-surface min-h-screen">
      {/* Page Header */}
      <div className="bg-white border-b border-border">
        <div className="container-grid py-10">
          <h1 className="text-display text-text mb-3">Маршруты</h1>
          <p className="text-body-lg text-text-secondary max-w-2xl">
            Готовые маршруты по доступным местам с подробным описанием
          </p>
        </div>
      </div>

      {/* Routes Grid */}
      <div className="container-grid py-8">
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {MOCK_ROUTES.map((route) => (
            <RouteCard key={route.id} route={route} />
          ))}
        </div>
      </div>
    </div>
  );
}