import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDistance(km: number): string {
  if (km < 1) return `${Math.round(km * 1000)} м`;
  return `${km.toFixed(1)} км`;
}

export function formatDuration(days: number): string {
  if (days === 1) return "1 день";
  return `${days} дня`;
}

export const CATEGORY_LABELS: Record<string, string> = {
  hotel: "Отель",
  restaurant: "Ресторан",
  attraction: "Достопримечательность",
  transport: "Транспорт",
  service: "Сервис",
};

export const DIFFICULTY_LABELS: Record<string, string> = {
  easy: "Лёгкий",
  medium: "Средний",
  hard: "Сложный",
};