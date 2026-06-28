"use client";

import { FormEvent, useState } from "react";

import { API_BASE_URL, PredictionResponse, predictImage } from "@/lib/api";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setPrediction(null);

    if (!selectedFile) {
      setError("Vui lòng chọn một ảnh lá cây trước khi gửi.");
      return;
    }

    setIsSubmitting(true);
    try {
      const result = await predictImage(selectedFile);
      setPrediction(result);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Không thể gửi ảnh để dự đoán.");
    } finally {
      setIsSubmitting(false);
    }
  }

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
          <form className="rounded-lg border border-dashed border-emerald-300 bg-white p-5 shadow-sm" onSubmit={handleSubmit}>
            <label className="flex min-h-72 cursor-pointer flex-col items-center justify-center gap-3 rounded-md bg-emerald-50 px-4 text-center transition hover:bg-emerald-100">
              <span className="text-lg font-medium text-stone-950">Chọn hoặc kéo ảnh lá cây</span>
              <span className="text-sm text-stone-600">PNG, JPG hoặc WEBP</span>
              <input
                className="sr-only"
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={(event) => {
                  setSelectedFile(event.target.files?.[0] ?? null);
                  setError(null);
                }}
              />
              {selectedFile ? (
                <span className="max-w-full break-all text-sm font-medium text-emerald-800">{selectedFile.name}</span>
              ) : null}
            </label>
            <button
              className="mt-4 w-full rounded-md bg-emerald-700 px-4 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-stone-400"
              disabled={isSubmitting}
              type="submit"
            >
              {isSubmitting ? "Đang gửi ảnh..." : "Gửi ảnh để dự đoán"}
            </button>
            {error ? (
              <p className="mt-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800">{error}</p>
            ) : null}
          </form>

          <aside className="rounded-lg border border-stone-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-stone-950">Kết quả</h2>
            <dl className="mt-4 grid gap-3 text-sm">
              <div className="flex justify-between gap-4">
                <dt className="text-stone-600">API</dt>
                <dd className="break-all text-right font-medium text-stone-900">{API_BASE_URL}</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-stone-600">Nhãn</dt>
                <dd className="text-right font-medium text-stone-900">
                  {prediction?.recommendation?.name_vi ?? prediction?.prediction ?? "Chưa có dự đoán"}
                </dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-stone-600">Confidence</dt>
                <dd className="font-medium text-stone-900">
                  {prediction ? `${Math.round(prediction.confidence * 100)}%` : "--"}
                </dd>
              </div>
            </dl>

            {prediction?.top_k?.length ? (
              <div className="mt-5 border-t border-stone-200 pt-4">
                <h3 className="text-sm font-semibold text-stone-950">Top dự đoán</h3>
                <ul className="mt-2 grid gap-2 text-sm text-stone-700">
                  {prediction.top_k.map((item) => (
                    <li className="flex justify-between gap-3" key={item.label}>
                      <span>{item.label}</span>
                      <span className="font-medium text-stone-900">{Math.round(item.confidence * 100)}%</span>
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}

            {prediction?.recommendation ? (
              <section className="mt-5 border-t border-stone-200 pt-4">
                <h3 className="text-sm font-semibold text-stone-950">Khuyến nghị xử lý</h3>
                {prediction.recommendation.confidence_note ? (
                  <p className="mt-2 text-sm text-amber-800">{prediction.recommendation.confidence_note}</p>
                ) : null}
                <p className="mt-2 text-sm text-stone-700">{prediction.recommendation.description}</p>
                <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-stone-700">
                  {prediction.recommendation.treatments.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
                {prediction.recommendation.advisory ? (
                  <p className="mt-3 text-xs text-stone-500">{prediction.recommendation.advisory}</p>
                ) : null}
              </section>
            ) : null}
          </aside>
        </div>
      </section>
    </main>
  );
}
