import Link from "next/link";
import type { Place } from "@/types/place";

interface PlaceCardProps {
  place: Place;
}

function getAccessibilityLevel(
  accessibility: Place["accessibility"]
): "full" | "partial" | "none" | null {
  if (!accessibility) return null;
  const a = accessibility;
  const hasStepFree = a.has_step_free_entrance;
  const hasRamp = a.has_ramp;
  const hasElevator = a.has_elevator;
  const hasWc = a.has_accessible_wc;
  const hasParking = a.has_accessible_parking;

  const positives = [hasStepFree, hasRamp, hasElevator, hasWc, hasParking].filter(
    (v) => v === true
  ).length;
  const negatives = [hasStepFree, hasRamp, hasElevator, hasWc, hasParking].filter(
    (v) => v === false
  ).length;

  if (negatives === 0 && positives >= 3) return "full";
  if (positives >= 2) return "partial";
  return "none";
}

export function PlaceCard({ place }: PlaceCardProps) {
  const level = getAccessibilityLevel(place.accessibility);

  const accessibilityLabels: Record<string, string> = {
    full: "Полная",
    partial: "Частичная",
    none: "Нет доступа",
  };

  const categoryLabels: Record<string, string> = {
    hotel: "Отель",
    restaurant: "Ресторан",
    attraction: "Достопримечательность",
    transport: "Транспорт",
    service: "Сервис",
  };

  const thumbnail = place.media?.[0]?.thumbnail_url || place.media?.[0]?.url;

  return (
    <Link href={`/places/${place.slug}`} className="card group flex flex-col">
      {/* Image */}
      <div className="aspect-[16/10] bg-surface rounded-t-xl flex items-center justify-center overflow-hidden">
        {thumbnail ? (
          <img
            src={thumbnail}
            alt={place.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <svg
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#C1C9D2"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
            <circle cx="12" cy="10" r="3" />
          </svg>
        )}
      </div>

      {/* Content */}
      <div className="flex-1 p-5 flex flex-col gap-3">
        <div className="flex items-start justify-between gap-2">
          <h3 className="text-h4 text-text group-hover:text-primary transition-colors line-clamp-1">
            {place.name}
          </h3>
          {place.avg_rating != null && (
            <span className="flex items-center gap-1 text-body-sm font-semibold text-primary shrink-0">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
              </svg>
              {place.avg_rating.toFixed(1)}
            </span>
          )}
        </div>

        <p className="text-body-sm text-text-secondary line-clamp-1">
          {place.address}
        </p>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mt-auto">
          <span className="badge-primary">
            {categoryLabels[place.category] || place.category}
          </span>
          {level && (
            <span
              className={
                level === "full"
                  ? "badge-success"
                  : level === "partial"
                  ? "badge-warning"
                  : "badge-neutral"
              }
            >
              {accessibilityLabels[level]}
            </span>
          )}
          {place.is_verified && (
            <span className="badge-success">✓ Проверено</span>
          )}
        </div>
      </div>
    </Link>
  );
}