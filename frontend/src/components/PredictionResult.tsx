"use client";

import React from "react";
import { PredictionResponse } from "../lib/api";

interface PredictionResultProps {
  prediction: PredictionResponse;
}

export default function PredictionResult({ prediction }: PredictionResultProps) {
  const {
    prediction: rawLabel,
    confidence,
    recommendation,
    latency_ms,
    prediction_id,
  } = prediction;

  const diseaseNameVi = recommendation?.name_vi || rawLabel;
  const confidencePercent = Math.round(confidence * 100);
  const confidenceNote = recommendation?.confidence_note;

  return (
    <div className="w-full p-5 bg-white border border-stone-200 rounded-xl shadow-sm space-y-4">
      <div className="flex flex-col gap-1 border-b border-stone-100 pb-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-stone-400">
          Kết quả chẩn đoán
        </span>
        <h3 className="text-2xl font-bold text-stone-900 leading-tight">
          {diseaseNameVi}
        </h3>
        {recommendation?.name_en && (
          <p className="text-sm text-stone-500 italic">
            {recommendation.name_en}
          </p>
        )}
        <div className="mt-1 flex flex-wrap gap-2 items-center">
          <code className="text-xs px-2 py-0.5 bg-stone-100 text-stone-600 rounded">
            Nhãn: {rawLabel}
          </code>
          {recommendation?.crop && (
            <span className="text-xs px-2 py-0.5 bg-healthy-50 text-healthy-700 font-medium rounded-full border border-healthy-100/50">
              Cây trồng: {recommendation.crop === "rice" ? "Lúa" : recommendation.crop === "coffee" ? "Cà phê" : recommendation.crop}
            </span>
          )}
          {recommendation?.severity && (
            <span className={`text-xs px-2 py-0.5 font-medium rounded-full border ${
              recommendation.severity.toLowerCase() === "high" || recommendation.severity.toLowerCase() === "severe"
                ? "bg-danger-50 text-danger-700 border-danger-100/50"
                : recommendation.severity.toLowerCase() === "medium" || recommendation.severity.toLowerCase() === "moderate"
                ? "bg-warning-50 text-warning-700 border-warning-100/50"
                : "bg-healthy-50 text-healthy-700 border-healthy-100/50"
            }`}>
              Mức độ: {recommendation.severity === "high" || recommendation.severity === "severe" ? "Nặng" : recommendation.severity === "medium" || recommendation.severity === "moderate" ? "Trung bình" : "Nhẹ"}
            </span>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="flex flex-col p-3 bg-stone-50 rounded-lg">
          <span className="text-xs text-stone-500 font-medium">Độ tin cậy</span>
          <span className="text-3xl font-extrabold text-healthy-700 mt-1">
            {confidencePercent}%
          </span>
        </div>

        <div className="flex flex-col p-3 bg-stone-50 rounded-lg justify-center">
          <span className="text-xs text-stone-500 font-medium">Thời gian xử lý</span>
          <span className="text-lg font-bold text-stone-800 mt-1">
            {latency_ms ? `${latency_ms.toFixed(0)} ms` : "--"}
          </span>
        </div>
      </div>

      {confidenceNote && (
        <div className="p-3 bg-warning-50/75 border border-warning-100/50 text-warning-700 rounded-lg text-xs font-medium">
          💡 {confidenceNote}
        </div>
      )}

      {prediction_id && (
        <div className="text-[10px] text-stone-400 text-right font-mono truncate">
          ID: {prediction_id}
        </div>
      )}
    </div>
  );
}
