import Link from "next/link";
import type { Route } from "@/types/route";

interface RouteCardProps {
  route: Route;
}

export function RouteCard({ route }: RouteCardProps) {
  const difficultyLabels: Record<string, string> = {
    easy: "Лёгкий",
    medium: "Средний",
    hard: "Сложный",
  };

  const difficultyColors: Record<string, string> = {
    easy: "badge-success",
    medium: "badge-warning",
    hard: "badge-neutral",
  };

  const placesCount = route.places?.length ?? 0;

  return (
    <Link href={`/routes/${route.slug}`} className="card group flex flex-col">
      {/* Header bar */}
      <div className="h-2 bg-primary rounded-t-xl" />

      {/* Content */}
      <div className="flex-1 p-5 flex flex-col gap-4">
        <div>
          <h3 className="text-h4 text-text group-hover:text-primary transition-colors line-clamp-2">
            {route.title}
          </h3>
          {route.description && (
            <p className="text-body-sm text-text-secondary mt-1.5 line-clamp-2">
              {route.description}
            </p>
          )}
        </div>

        {/* Stats grid */}
        <div className="grid grid-cols-3 gap-3 py-3 border-y border-border">
          <div className="text-center">
            <p className="text-h4 text-primary">
              {route.distance_km != null ? route.distance_km : "—"}
            </p>
            <p className="text-body-sm text-text-secondary">км</p>
          </div>
          <div className="text-center">
            <p className="text-h4 text-primary">{route.duration_days}</p>
            <p className="text-body-sm text-text-secondary">дней</p>
          </div>
          <div className="text-center">
            <p className="text-h4 text-primary">{placesCount || "—"}</p>
            <p className="text-body-sm text-text-secondary">мест</p>
          </div>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mt-auto">
          {route.difficulty && (
            <span className={difficultyColors[route.difficulty] || "badge-neutral"}>
              {difficultyLabels[route.difficulty] || route.difficulty}
            </span>
          )}
          {route.is_editorial && (
            <span className="badge-primary">Выбор редакции</span>
          )}
          {route.is_free && (
            <span className="badge-success">Бесплатно</span>
          )}
        </div>
      </div>
    </Link>
  );
}