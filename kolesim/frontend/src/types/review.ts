export interface Review {
  id: string;
  user_id: string;
  entity_type: "place" | "route";
  entity_id: string;
  rating: number;
  accessibility_rating: number;
  text: string | null;
  visited_at: string | null;
  wheelchair_type: string | null;
  moderation_status: "pending" | "approved" | "rejected";
  created_at: string;
  user?: {
    id: string;
    full_name: string;
  };
}

export interface ReviewCreate {
  entity_type: "place" | "route";
  entity_id: string;
  rating: number;
  accessibility_rating: number;
  text?: string;
  visited_at?: string;
  wheelchair_type?: string;
}