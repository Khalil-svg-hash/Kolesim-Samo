"use client";

import { useAuthStore } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function ProfilePage() {
  const router = useRouter();
  const { user, logout } = useAuthStore();

  useEffect(() => {
    if (!user) router.push("/login");
  }, [user, router]);

  if (!user) return null;

  return (
    <div className="bg-surface min-h-screen">
      {/* Page Header */}
      <div className="bg-white border-b border-border">
        <div className="container-grid py-10">
          <h1 className="text-display text-text mb-3">Профиль</h1>
          <p className="text-body-lg text-text-secondary">
            Управление аккаунтом и настройками
          </p>
        </div>
      </div>

      <div className="container-grid py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* User Info Card */}
          <div className="card p-6">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center">
                <span className="text-h2 text-primary">
                  {user.full_name?.[0]?.toUpperCase() || "U"}
                </span>
              </div>
              <div>
                <h2 className="text-h4 text-text">{user.full_name}</h2>
                <p className="text-body-sm text-text-secondary">{user.email}</p>
              </div>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between py-2 border-b border-border">
                <span className="text-body-sm text-text-secondary">Роль</span>
                <span className="badge-primary">
                  {user.is_admin ? "Администратор" : "Пользователь"}
                </span>
              </div>
              <div className="flex items-center justify-between py-2 border-b border-border">
                <span className="text-body-sm text-text-secondary">Подписка</span>
                <span className={user.subscription_status === "premium" ? "badge-primary" : "badge-neutral"}>
                  {user.subscription_status === "premium" ? "Премиум" : "Бесплатная"}
                </span>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="lg:col-span-2 space-y-6">
            <div className="card p-6">
              <h3 className="text-h3 text-text mb-4">Быстрые действия</h3>
              <div className="grid sm:grid-cols-2 gap-4">
                <a href="/places" className="card p-4 hover:border-primary transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center text-primary">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
                        <circle cx="12" cy="10" r="3" />
                      </svg>
                    </div>
                    <div>
                      <p className="text-body font-semibold text-text">Места</p>
                      <p className="text-body-sm text-text-secondary">Найти доступные места</p>
                    </div>
                  </div>
                </a>
                <a href="/routes" className="card p-4 hover:border-primary transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center text-primary">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                      </svg>
                    </div>
                    <div>
                      <p className="text-body font-semibold text-text">Маршруты</p>
                      <p className="text-body-sm text-text-secondary">Просмотреть маршруты</p>
                    </div>
                  </div>
                </a>
              </div>
            </div>

            <div className="card p-6">
              <h3 className="text-h3 text-text mb-4">Сохранённые</h3>
              <p className="text-body text-text-secondary">
                Здесь будут отображаться сохранённые места и маршруты
              </p>
            </div>

            <div className="flex gap-4">
              <button
                onClick={() => {
                  logout();
                  router.push("/");
                }}
                className="btn-secondary"
              >
                Выйти из аккаунта
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}