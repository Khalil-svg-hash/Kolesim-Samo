"use client";

import Link from "next/link";
import { useAuthStore } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function Header() {
  const { user, logout } = useAuthStore();
  const router = useRouter();

  const handleLogout = async () => {
    await logout();
    router.push("/");
  };

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/80 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <Link href="/" className="text-lg font-semibold text-slate-900">
          Колесим
        </Link>
        <nav className="flex items-center gap-6 text-sm">
          <Link href="/places" className="text-slate-600 hover:text-slate-900">
            Места
          </Link>
          <Link href="/routes" className="text-slate-600 hover:text-slate-900">
            Маршруты
          </Link>
          {user ? (
            <>
              <Link href="/profile" className="text-slate-600 hover:text-slate-900">
                Профиль
              </Link>
              <button onClick={handleLogout} className="text-slate-600 hover:text-slate-900">
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="text-slate-600 hover:text-slate-900">
                Войти
              </Link>
              <Link href="/register" className="btn-primary text-sm">
                Регистрация
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}