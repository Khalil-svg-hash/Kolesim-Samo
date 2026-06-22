import Link from "next/link";

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
            <Link href="/routes" className="btn-primary">
              Смотреть маршруты
            </Link>
            <Link href="/places" className="btn-outline">
              Каталог мест
            </Link>
          </div>
        </div>
      </section>

      <section className="bg-slate-100">
        <div className="mx-auto grid max-w-6xl gap-6 px-6 py-16 md:grid-cols-3">
          {[
            {
              title: "Ложная доступность",
              text: "Проверяем вход, ширину дверей и реальный маршрут до объекта.",
            },
            {
              title: "Дни на проверку",
              text: "Собираем подтвержденные данные и замеры на месте.",
            },
            {
              title: "Риск разочарования",
              text: "Даем прозрачную картину до поездки и экономим время.",
            },
          ].map((item) => (
            <div key={item.title} className="card">
              <h3 className="text-lg font-semibold text-slate-900">{item.title}</h3>
              <p className="mt-2 text-sm text-slate-600">{item.text}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-white">
        <div className="mx-auto max-w-6xl px-6 py-16">
          <h2 className="text-2xl font-semibold text-slate-900">Как это работает</h2>
          <div className="mt-8 grid gap-8 md:grid-cols-3">
            {[
              { step: "1", title: "Найдите место", text: "Ищите в каталоге по категории, городу и доступности." },
              { step: "2", title: "Проверьте доступность", text: "Смотрите замеры дверей, наличие лифта и парковки." },
              { step: "3", title: "Спланируйте маршрут", text: "Соберите маршрут из проверенных мест на 1-2 дня." },
            ].map((item) => (
              <div key={item.step} className="flex gap-4">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-brand-primary text-white">
                  {item.step}
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900">{item.title}</h3>
                  <p className="mt-1 text-sm text-slate-600">{item.text}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}