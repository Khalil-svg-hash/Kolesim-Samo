import Link from "next/link";

export default function HomePage() {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-white">
        <div className="container-grid py-20 lg:py-28">
          <div className="max-w-3xl">
            <div className="badge-primary mb-6">
              Платформа доступного туризма
            </div>
            <h1 className="text-display text-text mb-6">
              Доступные путешествия для&nbsp;всех
            </h1>
            <p className="text-body-lg text-text-secondary mb-10 max-w-2xl">
              Находите проверенные места и маршруты с полной информацией о
              доступности для людей с ограниченной подвижностью. Путешествуйте
              уверенно.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link href="/places" className="btn-primary">
                Найти место
              </Link>
              <Link href="/routes" className="btn-secondary">
                Смотреть маршруты
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Bar */}
      <section className="bg-primary">
        <div className="container-grid py-10">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {[
              { value: "1 200+", label: "Доступных мест" },
              { value: "85", label: "Маршрутов" },
              { value: "45", label: "Городов" },
              { value: "5 000+", label: "Пользователей" },
            ].map((stat) => (
              <div key={stat.label}>
                <p className="text-h2 text-white">{stat.value}</p>
                <p className="text-body-sm text-white/70 mt-1">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-surface">
        <div className="container-grid py-20">
          <h2 className="section-title text-center mb-4">
            Как это работает
          </h2>
          <p className="text-body-lg text-text-secondary text-center max-w-2xl mx-auto mb-14">
            Три простых шага к доступному путешествию
          </p>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: "01",
                title: "Найдите место",
                description:
                  "Ищите кафе, музеи, парки и другие места с подробной информацией о доступности",
                icon: (
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="11" cy="11" r="8" /><path d="m21 21-4.3-4.3" />
                  </svg>
                ),
              },
              {
                step: "02",
                title: "Проверьте доступность",
                description:
                  "Узнайте о пандусах, лифтах, доступных туалетах и парковках перед визитом",
                icon: (
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" />
                  </svg>
                ),
              },
              {
                step: "03",
                title: "Выберите маршрут",
                description:
                  "Составьте маршрут из доступных мест или выберите готовый от нашей команды",
                icon: (
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                  </svg>
                ),
              },
            ].map((item) => (
              <div key={item.step} className="card p-8">
                <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center text-primary mb-5">
                  {item.icon}
                </div>
                <div className="text-body-sm font-semibold text-primary mb-2">
                  Шаг {item.step}
                </div>
                <h3 className="text-h3 text-text mb-3">{item.title}</h3>
                <p className="text-body text-text-secondary">
                  {item.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Accessibility Info Section */}
      <section className="bg-white">
        <div className="container-grid py-20">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="section-title mb-6">
                Подробная информация о доступности
              </h2>
              <p className="text-body-lg text-text-secondary mb-8">
                Для каждого места мы собираем и проверяем данные о доступности,
                чтобы вы могли спланировать поездку без сюрпризов.
              </p>
              <ul className="space-y-4">
                {[
                  "Беспороговый вход и ширина дверей",
                  "Наличие пандусов и лифтов",
                  "Доступные туалетные комнаты",
                  "Парковочные места для инвалидов",
                  "Тип покрытия пола и дополнительные заметки",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-3">
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="#0F62FE"
                      strokeWidth="2.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="shrink-0 mt-0.5"
                    >
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                    <span className="text-body text-text">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="bg-surface rounded-2xl p-8">
              <div className="space-y-4">
                {[
                  { label: "Беспороговый вход", value: true },
                  { label: "Ширина двери входа", value: "90 см" },
                  { label: "Пандус", value: true },
                  { label: "Лифт", value: false },
                  { label: "Доступный туалет", value: true },
                  { label: "Парковка", value: true },
                ].map((item) => (
                  <div
                    key={item.label}
                    className="flex items-center justify-between py-3 border-b border-border last:border-0"
                  >
                    <span className="text-body text-text">{item.label}</span>
                    {typeof item.value === "boolean" ? (
                      <span
                        className={
                          item.value ? "badge-success" : "badge-neutral"
                        }
                      >
                        {item.value ? "Да" : "Нет"}
                      </span>
                    ) : (
                      <span className="text-body font-semibold text-text">
                        {item.value}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary">
        <div className="container-grid py-20 text-center">
          <h2 className="text-h2 text-white mb-4">
            Начните путешествовать уже сегодня
          </h2>
          <p className="text-body-lg text-white/70 max-w-xl mx-auto mb-8">
            Присоединяйтесь к сообществу и делитесь отзывами о доступности мест
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              href="/register"
              className="inline-flex items-center justify-center px-6 py-3 bg-white text-primary font-semibold rounded-lg hover:bg-surface transition-colors duration-200"
            >
              Создать аккаунт
            </Link>
            <Link
              href="/places"
              className="inline-flex items-center justify-center px-6 py-3 bg-transparent text-white font-semibold rounded-lg border-2 border-white/30 hover:bg-white/10 transition-colors duration-200"
            >
              Смотреть места
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-text">
        <div className="container-grid py-12">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-2.5">
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
              <span className="text-xl font-bold text-white tracking-tight">
                Колесим
              </span>
            </div>
            <p className="text-body-sm text-white/50">
              © 2024 Колесим. Платформа доступного туризма.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}