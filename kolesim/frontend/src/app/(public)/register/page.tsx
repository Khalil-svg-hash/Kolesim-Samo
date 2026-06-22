"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/lib/auth";

export default function RegisterPage() {
  const router = useRouter();
  const register = useAuthStore((s) => s.register);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      await register(email, password, name);
      router.push("/profile");
    } catch {
      setError("Ошибка регистрации. Попробуйте снова.");
    }
  };

  return (
    <div className="bg-surface min-h-screen flex items-center justify-center py-12 px-4">
      <div className="w-full max-w-md">
        <div className="card p-8">
          <div className="text-center mb-8">
            <div className="w-12 h-12 bg-primary rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <path d="M12 6v6l4 2" />
              </svg>
            </div>
            <h1 className="text-h2 text-text mb-2">Регистрация</h1>
            <p className="text-body text-text-secondary">
              Создайте аккаунт для сохранения мест и маршрутов
            </p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 text-body-sm rounded-lg px-4 py-3 mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-body-sm font-medium text-text mb-1.5">
                Имя
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="input-field"
                placeholder="Ваше имя"
              />
            </div>
            <div>
              <label className="block text-body-sm font-medium text-text mb-1.5">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="input-field"
                placeholder="you@example.com"
              />
            </div>
            <div>
              <label className="block text-body-sm font-medium text-text mb-1.5">
                Пароль
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={8}
                className="input-field"
                placeholder="Минимум 8 символов"
              />
            </div>
            <button type="submit" className="btn-primary w-full">
              Создать аккаунт
            </button>
          </form>

          <p className="text-body-sm text-text-secondary text-center mt-6">
            Уже есть аккаунт?{" "}
            <Link href="/login" className="text-primary font-semibold hover:underline">
              Войти
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}