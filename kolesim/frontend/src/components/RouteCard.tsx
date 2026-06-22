"use client";

import Link from "next/link";
import type { Route } from "@/types/route";
import { formatDistance, formatDuration, DIFFICULTY_LABELS } from "@/lib/utils";

interface RouteCardProps {
  route: Route;
}

export default function RouteCard({ route }: RouteCardProps) {
  return (
    <Link href={`/routes/${route.slug}`} className="group">
      <div className="card transition-shadow group-hover:shadow-md">
        <div className="flex items-start justify-between">
          <div>
            <span className="inline-block rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-brand-primary">
              {formatDuration(route.duration_days)}
            </span>
            <h3 className="mt-2 text-lg font-semibold text-slate-900">{route.title}</h3>
          </div>
          {route.is_free && (
            <span className="rounded-full bg-green-50 px-2 py-1 text-xs text-green-700">
              Бесплатно
            </span>
          )}
        </div>
        {route.description && (
          <p className="mt-2 text-sm text-slate-600 line-clamp-2">{route.description}</p>
        )}
        <div className="mt-3 flex flex-wrap gap-3 text-sm text-slate-500">
          {route.distance_km && <span>📏 {formatDistance(route.distance_km)}</span>}
          {route.difficulty && <span>💪 {DIFFICULTY_LABELS[route.difficulty] || route.difficulty}</span>}
          <span>👁 {route.view_count}</span>
        </div>
        {route.tags && route.tags.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1">
            {route.tags.map((tag) => (
              <span key={tag} className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </Link>
  );
}