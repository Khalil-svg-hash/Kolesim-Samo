export interface Accessibility {
  has_step_free_entrance: boolean | null;
  entrance_door_width_cm: number | null;
  has_ramp: boolean | null;
  has_elevator: boolean | null;
  elevator_door_width_cm: number | null;
  has_accessible_wc: boolean | null;
  wc_door_width_cm: number | null;
  has_accessible_parking: boolean | null;
  parking_distance_m: number | null;
  floor_surface: string | null;
  extra_notes: string | null;
}

export interface Media {
  id: string;
  entity_type: string;
  entity_id: string;
  url: string;
  thumbnail_url: string | null;
  caption: string | null;
  media_type: string;
  sort_order: number;
  created_at: string;
}

export interface Place {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  category: "hotel" | "restaurant" | "attraction" | "transport" | "service";
  address: string;
  city: string;
  latitude: number;
  longitude: number;
  entrance_lat: number | null;
  entrance_lng: number | null;
  parking_lat: number | null;
  parking_lng: number | null;
  price_level: 1 | 2 | 3 | null;
  is_verified: boolean;
  verified_at: string | null;
  is_free: boolean;
  is_published: boolean;
  media: Media[];
  accessibility: Accessibility | null;
  avg_rating: number | null;
  review_count: number;
  created_at: string;
}

export interface PlaceListResponse {
  items: Place[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}
