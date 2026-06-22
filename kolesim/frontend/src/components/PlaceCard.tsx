"use client";

import Link from "next/link";
import type { Place } from "@/types/place";
import { CATEGORY_LABELS } from "@/lib/utils";

interface PlaceCardProps {
  place: Place;
}

export default function PlaceCard({ place }: PlaceCardProps) {
  return (
    <Link href={`/places/${place.slug}`} className="group">
      <div className="card transition-shadow group-hover:shadow-md">
        <div className="flex items-start justify-between">
          <div>
            <span className="inline-block rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-brand-primary">
              {CATEGORY_LABELS[place.category] || place.category}
            </span>
            <h3 className="mt-2 text-lg font-semibold text-slate-900">{place.name}</h3>
            <p className="mt-1 text-sm text-slate-500">{place.address}</p>
          </div>
          {place.is_verified && (
            <span className="rounded-full bg-green-50 px-2 py-1 text-xs text-green-700">
              ✓ Проверено
            </span>
          )}
        </div>
        {place.accessibility && (
          <div className="mt-3 flex flex-wrap gap-2">
            {place.accessibility.has_step_free_entrance && (
              <span className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
                Без ступеней
              </span>
            )}
            {place.accessibility.has_elevator && (
              <span className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
                Лифт
              </span>
            )}
            {place.accessibility.has_accessible_wc && (
              <span className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
                Доступный туалет
              </span>
            )}
            {place.accessibility.has_accessible_parking && (
              <span className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
                Парковка
              </span>
            )}
          </div>
        )}
        {place.avg_rating !== null && (
          <div className="mt-3 text-sm text-slate-600">
            ⭐ {place.avg_rating.toFixed(1)} ({place.review_count})
          </div>
        )}
      </div>
    </Link>
  );
}