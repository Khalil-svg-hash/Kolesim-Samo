export default function HomePage() {
  return (
    <main className="min-h-screen">
      <section className="bg-white">
        <div className="mx-auto max-w-6xl px-6 py-20">
          <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Колесим самостоятельно</p>
          <h1 className="mt-4 text-4xl font-semibold leading-tight text-slate-900 md:text-5xl">
            Путешествуй на коляске. Без сюрпризов.
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-slate-600">
            Каталог проверенных доступных мест и конструктор маршрутов для Москвы и области.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <button className="rounded-full bg-brand-primary px-6 py-3 text-white">
              Смотреть маршруты
            </button>
            <button className="rounded-full border border-slate-200 px-6 py-3 text-slate-700">
              Начать бесплатно
            </button>
          </div>
        </div>
      </section>
      <section className="bg-slate-100">
        <div className="mx-auto grid max-w-6xl gap-6 px-6 py-16 md:grid-cols-3">
          {[
            {
              title: "Ложная доступность",
              text: "Проверяем вход, ширину дверей и реальный маршрут до объекта."
            },
            {
              title: "Дни на проверку",
              text: "Собираем подтвержденные данные и замеры на месте."
            },
            {
              title: "Риск разочарования",
              text: "Даем прозрачную картину до поездки и экономим время."
            }
          ].map((item) => (
            <div key={item.title} className="rounded-2xl bg-white p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-slate-900">{item.title}</h3>
              <p className="mt-2 text-sm text-slate-600">{item.text}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
