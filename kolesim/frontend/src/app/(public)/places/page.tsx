"use client";

import { useState } from "react";
import { PlaceCard } from "@/components/PlaceCard";
import type { Place } from "@/types/place";

const MOCK_PLACES: Place[] = [
  {
    id: "1",
    name: "Кафе «Доступный мир»",
    slug: "dostupnyy-mir",
    description: "Уютное кафе с полным доступом",
    category: "restaurant",
    address: "ул. Пушкина, 10",
    city: "Москва",
    latitude: 55.75,
    longitude: 37.62,
    entrance_lat: null,
    entrance_lng: null,
    parking_lat: null,
    parking_lng: null,
    price_level: 2,
    is_verified: true,
    verified_at: "2024-01-01",
    is_free: false,
    is_published: true,
    media: [],
    accessibility: {
      has_step_free_entrance: true,
      entrance_door_width_cm: 90,
      has_ramp: true,
      has_elevator: false,
      elevator_door_width_cm: null,
      has_accessible_wc: true,
      wc_door_width_cm: 85,
      has_accessible_parking: true,
      parking_distance_m: 20,
      floor_surface: "tile",
      extra_notes: null,
    },
    avg_rating: 4.5,
    review_count: 12,
    created_at: "2024-01-01",
  },
  {
    id: "2",
    name: "Музей «Открытый город»",
    slug: "otkrytyy-gorod",
    description: "Музей с полной доступностью",
    category: "attraction",
    address: "пр. Мира, 25",
    city: "Санкт-Петербург",
    latitude: 59.93,
    longitude: 30.32,
    entrance_lat: null,
    entrance_lng: null,
    parking_lat: null,
    parking_lng: null,
    price_level: 1,
    is_verified: true,
    verified_at: "2024-02-01",
    is_free: false,
    is_published: true,
    media: [],
    accessibility: {
      has_step_free_entrance: true,
      entrance_door_width_cm: 100,
      has_ramp: true,
      has_elevator: true,
      elevator_door_width_cm: 90,
      has_accessible_wc: true,
      wc_door_width_cm: 90,
      has_accessible_parking: true,
      parking_distance_m: 15,
      floor_surface: "tile",
      extra_notes: null,
    },
    avg_rating: 4.8,
    review_count: 28,
    created_at: "2024-02-01",
  },
  {
    id: "3",
    name: "Парк «Равные возможности»",
    slug: "ravnye-vozmozhnosti",
    description: "Городской парк с адаптированными дорожками",
    category: "attraction",
    address: "ул. Садовая, 5",
    city: "Казань",
    latitude: 55.79,
    longitude: 49.11,
    entrance_lat: null,
    entrance_lng: null,
    parking_lat: null,
    parking_lng: null,
    price_level: null,
    is_verified: false,
    verified_at: null,
    is_free: true,
    is_published: true,
    media: [],
    accessibility: {
      has_step_free_entrance: true,
      entrance_door_width_cm: null,
      has_ramp: false,
      has_elevator: null,
      elevator_door_width_cm: null,
      has_accessible_wc: false,
      wc_door_width_cm: null,
      has_accessible_parking: true,
      parking_distance_m: 50,
      floor_surface: "asphalt",
      extra_notes: "Асфальтированные дорожки",
    },
    avg_rating: 3.9,
    review_count: 5,
    created_at: "2024-03-01",
  },
];

const CATEGORIES = [
  { value: "", label: "Все категории" },
  { value: "hotel", label: "Отели" },
  { value: "restaurant", label: "Рестораны" },
  { value: "attraction", label: "Достопримечательности" },
  { value: "transport", label: "Транспорт" },
  { value: "service", label: "Сервис" },
];

export default function PlacesPage() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");

  const filtered = MOCK_PLACES.filter((p) => {
    const matchSearch =
      !search ||
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      p.address.toLowerCase().includes(search.toLowerCase());
    const matchCategory = !category || p.category === category;
    return matchSearch && matchCategory;
  });

  return (
    <div className="bg-surface min-h-screen">
      {/* Page Header */}
      <div className="bg-white border-b border-border">
        <div className="container-grid py-10">
          <h1 className="text-display text-text mb-3">Доступные места</h1>
          <p className="text-body-lg text-text-secondary max-w-2xl">
            Находите проверенные места с подробной информацией о доступности
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white border-b border-border">
        <div className="container-grid py-4">
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#6B7280"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="absolute left-3 top-1/2 -translate-y-1/2"
              >
                <circle cx="11" cy="11" r="8" />
                <path d="m21 21-4.3-4.3" />
              </svg>
              <input
                type="text"
                placeholder="Поиск по названию или адресу..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="input-field pl-10"
              />
            </div>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="input-field sm:w-56"
            >
              {CATEGORIES.map((c) => (
                <option key={c.value} value={c.value}>
                  {c.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Results */}
      <div className="container-grid py-8">
        <p className="text-body-sm text-text-secondary mb-6">
          Найдено мест: {filtered.length}
        </p>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((place) => (
            <PlaceCard key={place.id} place={place} />
          ))}
        </div>
        {filtered.length === 0 && (
          <div className="text-center py-20">
            <p className="text-h3 text-text-secondary mb-2">Ничего не найдено</p>
            <p className="text-body text-text-secondary">
              Попробуйте изменить параметры поиска
            </p>
          </div>
        )}
      </div>
    </div>
  );
}