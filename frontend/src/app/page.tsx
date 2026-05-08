const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export default function Home() {
  return (
    <main className="min-h-screen px-4 py-6 sm:px-8">
      <section className="mx-auto flex w-full max-w-5xl flex-col gap-6">
        <div className="flex flex-col gap-2 border-b border-stone-200 pb-4">
          <p className="text-sm font-medium uppercase tracking-normal text-emerald-700">
            Cà phê / Lúa
          </p>
          <h1 className="text-3xl font-semibold text-stone-950 sm:text-4xl">
            Chẩn đoán bệnh trên lá cây
          </h1>
          <p className="max-w-2xl text-base text-stone-700">
            Dành cho ảnh lá lúa và cà phê trong điều kiện thực địa tại Việt Nam.
          </p>
        </div>

        <div className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
          <form className="rounded-lg border border-dashed border-emerald-300 bg-white p-5 shadow-sm">
            <label className="flex min-h-72 cursor-pointer flex-col items-center justify-center gap-3 rounded-md bg-emerald-50 px-4 text-center">
              <span className="text-lg font-medium text-stone-950">Chọn hoặc kéo ảnh lá cây</span>
              <span className="text-sm text-stone-600">PNG, JPG hoặc WEBP</span>
              <input className="sr-only" type="file" accept="image/*" />
            </label>
            <button
              className="mt-4 w-full rounded-md bg-emerald-700 px-4 py-3 text-sm font-semibold text-white"
              type="button"
            >
              Gửi ảnh để dự đoán
            </button>
          </form>

          <aside className="rounded-lg border border-stone-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-stone-950">Kết quả</h2>
            <dl className="mt-4 grid gap-3 text-sm">
              <div className="flex justify-between gap-4">
                <dt className="text-stone-600">API</dt>
                <dd className="break-all text-right font-medium text-stone-900">{apiBaseUrl}</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-stone-600">Nhãn</dt>
                <dd className="font-medium text-stone-900">Chưa có dự đoán</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-stone-600">Confidence</dt>
                <dd className="font-medium text-stone-900">--</dd>
              </div>
            </dl>
          </aside>
        </div>
      </section>
    </main>
  );
}
