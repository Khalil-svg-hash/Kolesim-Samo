"use client";

import Link from "next/link";
import { useAuthStore } from "@/lib/auth";

export function Header() {
  const { user, logout } = useAuthStore();

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-border">
      <div className="container-grid flex items-center justify-between h-16">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="white"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="10" />
              <path d="M12 6v6l4 2" />
            </svg>
          </div>
          <span className="text-xl font-bold text-text tracking-tight">
            Колесим
          </span>
        </Link>

        {/* Navigation */}
        <nav className="hidden md:flex items-center gap-1">
          <Link href="/places" className="btn-ghost">
            Места
          </Link>
          <Link href="/routes" className="btn-ghost">
            Маршруты
          </Link>
        </nav>

        {/* Auth */}
        <div className="flex items-center gap-3">
          {user ? (
            <>
              <Link href="/profile" className="btn-ghost">
                Профиль
              </Link>
              <button onClick={logout} className="btn-ghost text-text-secondary">
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="btn-ghost">
                Войти
              </Link>
              <Link href="/register" className="btn-primary text-sm">
                Регистрация
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}