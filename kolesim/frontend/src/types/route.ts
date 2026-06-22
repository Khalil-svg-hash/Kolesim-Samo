export interface RoutePlace {
  id: string;
  route_id: string;
  place_id: string;
  order_index: number;
  day_number: number;
  notes: string | null;
  estimated_duration_min: number | null;
  place?: import("./place").Place;
}

export interface Route {
  id: string;
  title: string;
  slug: string;
  description: string | null;
  duration_days: 1 | 2;
  distance_km: number | null;
  difficulty: string | null;
  tags: string[] | null;
  is_editorial: boolean;
  is_published: boolean;
  is_free: boolean;
  view_count: number;
  created_by: string | null;
  created_at: string;
  updated_at: string;
  places?: RoutePlace[];
}

export interface RouteListResponse {
  items: Route[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}