"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import RouteCard from "@/components/RouteCard";
import type { Route, RouteListResponse } from "@/types/route";

export default function RoutesPage() {
  const [routes, setRoutes] = useState<Route[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/routes?limit=20")
      .then(({ data }) => setRoutes((data as RouteListResponse).items))
      .catch(() => setRoutes([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <h1 className="text-3xl font-semibold text-slate-900">Маршруты</h1>
      <p className="mt-2 text-slate-600">Готовые доступные маршруты на 1-2 дня</p>
      {loading ? (
        <p className="mt-10 text-center text-slate-400">Загрузка...</p>
      ) : routes.length === 0 ? (
        <p className="mt-10 text-center text-slate-400">Маршруты не найдены</p>
      ) : (
        <div className="mt-8 grid gap-6 sm:grid-cols-2">
          {routes.map((route) => (
            <RouteCard key={route.id} route={route} />
          ))}
        </div>
      )}
    </main>
  );
}