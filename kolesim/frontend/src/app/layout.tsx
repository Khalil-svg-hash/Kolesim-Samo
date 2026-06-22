import type { Metadata } from "next";
import { Manrope } from "next/font/google";
import "./globals.css";
import Providers from "@/components/Providers";
import Header from "@/components/Header";

const manrope = Manrope({ subsets: ["latin", "cyrillic"], display: "swap" });

export const metadata: Metadata = {
  title: "Колесим самостоятельно",
  description: "Каталог доступных мест и конструктор маршрутов для пользователей инвалидной коляски.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru" className={manrope.className}>
      <body className="bg-slate-50 text-slate-900">
        <Providers>
          <Header />
          {children}
        </Providers>
      </body>
    </html>
  );
}