"use client";

import { useAuthStore } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function ProfilePage() {
  const { user, isLoading, logout } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user) router.push("/login");
  }, [isLoading, user, router]);

  if (isLoading) return <p className="py-20 text-center text-slate-400">Загрузка...</p>;
  if (!user) return null;

  return (
    <main className="mx-auto max-w-2xl px-6 py-10">
      <h1 className="text-3xl font-semibold text-slate-900">Профиль</h1>
      <div className="mt-6 card space-y-4">
        <div>
          <p className="text-sm text-slate-500">Имя</p>
          <p className="text-lg font-medium text-slate-900">{user.full_name}</p>
        </div>
        <div>
          <p className="text-sm text-slate-500">Email</p>
          <p className="text-lg font-medium text-slate-900">{user.email}</p>
        </div>
        <div>
          <p className="text-sm text-slate-500">Подписка</p>
          <p className="text-lg font-medium text-slate-900">
            {user.subscription_status === "premium" ? "Premium" : "Бесплатная"}
          </p>
        </div>
        <div>
          <p className="text-sm text-slate-500">Статус</p>
          <p className="text-lg font-medium text-slate-900">
            {user.is_verified ? "✓ Подтверждён" : "Не подтверждён"}
          </p>
        </div>
      </div>
      <button
        onClick={async () => { await logout(); router.push("/"); }}
        className="mt-6 btn-outline"
      >
        Выйти из аккаунта
      </button>
    </main>
  );
}