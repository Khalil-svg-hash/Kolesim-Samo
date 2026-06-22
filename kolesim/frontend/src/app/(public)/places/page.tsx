"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import PlaceCard from "@/components/PlaceCard";
import type { Place, PlaceListResponse } from "@/types/place";

const CATEGORIES = [
  { value: "", label: "Все" },
  { value: "hotel", label: "Отели" },
  { value: "restaurant", label: "Рестораны" },
  { value: "attraction", label: "Достопримечательности" },
  { value: "transport", label: "Транспорт" },
  { value: "service", label: "Сервис" },
];

export default function PlacesPage() {
  const [places, setPlaces] = useState<Place[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [category, setCategory] = useState("");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams({ page: String(page), limit: "12" });
    if (category) params.set("category", category);
    if (search) params.set("search", search);
    api.get(`/places?${params}`)
      .then(({ data }) => {
        const resp = data as PlaceListResponse;
        setPlaces(resp.items);
        setTotal(resp.total);
      })
      .catch(() => setPlaces([]))
      .finally(() => setLoading(false));
  }, [page, category, search]);

  const pages = Math.ceil(total / 12);

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <h1 className="text-3xl font-semibold text-slate-900">Каталог мест</h1>
      <p className="mt-2 text-slate-600">Проверенные доступные места в Москве и области</p>

      <div className="mt-6 flex flex-wrap gap-3">
        <input
          type="text"
          placeholder="Поиск..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(1); }}
          className="rounded-full border border-slate-200 px-4 py-2 text-sm focus:border-brand-primary focus:outline-none"
        />
        {CATEGORIES.map((c) => (
          <button
            key={c.value}
            onClick={() => { setCategory(c.value); setPage(1); }}
            className={`rounded-full px-4 py-2 text-sm transition ${
              category === c.value
                ? "bg-brand-primary text-white"
                : "border border-slate-200 text-slate-600 hover:bg-slate-50"
            }`}
          >
            {c.label}
          </button>
        ))}
      </div>

      {loading ? (
        <p className="mt-10 text-center text-slate-400">Загрузка...</p>
      ) : places.length === 0 ? (
        <p className="mt-10 text-center text-slate-400">Места не найдены</p>
      ) : (
        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {places.map((place) => (
            <PlaceCard key={place.id} place={place} />
          ))}
        </div>
      )}

      {pages > 1 && (
        <div className="mt-8 flex justify-center gap-2">
          {Array.from({ length: pages }, (_, i) => (
            <button
              key={i}
              onClick={() => setPage(i + 1)}
              className={`rounded px-3 py-1 text-sm ${
                page === i + 1 ? "bg-brand-primary text-white" : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              {i + 1}
            </button>
          ))}
        </div>
      )}
    </main>
  );
}