import { create } from "zustand";
import api from "./api";
import type { User } from "@/types/user";

interface AuthState {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, full_name: string) => Promise<void>;
  logout: () => Promise<void>;
  fetchUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: true,

  login: async (email, password) => {
    const { data } = await api.post("/auth/login", { email, password });
    set({ user: data });
  },

  register: async (email, password, full_name) => {
    await api.post("/auth/register", { email, password, full_name });
  },

  logout: async () => {
    await api.post("/auth/logout");
    set({ user: null });
  },

  fetchUser: async () => {
    try {
      const { data } = await api.get("/users/me");
      set({ user: data, isLoading: false });
    } catch {
      set({ user: null, isLoading: false });
    }
  },
}));