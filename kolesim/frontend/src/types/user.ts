export interface User {
  id: string;
  email: string;
  full_name: string;
  is_verified: boolean;
  is_admin: boolean;
  subscription_status: "free" | "premium";
  created_at: string;
}

export interface AuthResponse {
  id: string;
  email: string;
  full_name: string;
  is_verified: boolean;
  is_admin: boolean;
  subscription_status: string;
}