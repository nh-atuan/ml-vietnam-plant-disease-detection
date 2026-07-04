"use client";

import React from "react";
import { TopKPrediction } from "../lib/api";

interface TopKListProps {
  topK: TopKPrediction[];
}

export default function TopKList({ topK }: TopKListProps) {
  if (!topK || topK.length === 0) return null;

  // Compute top-1 vs top-2 gap if we have at least 2 predictions
  const hasClosePrediction =
    topK.length >= 2 && topK[0].confidence - topK[1].confidence < 0.1;

  // Maximum confidence for scaling the bars proportionally (usually topK[0].confidence)
  const maxConfidence = topK[0].confidence || 1;

  return (
    <div className="w-full p-5 bg-white border border-stone-200 rounded-xl shadow-sm space-y-4">
      <div>
        <h4 className="text-sm font-semibold uppercase tracking-wider text-stone-400">
          Danh sách chẩn đoán hàng đầu
        </h4>
        <p className="text-xs text-stone-500 mt-0.5">
          So sánh độ tin cậy của các khả năng phân loại khác nhau
        </p>
      </div>

      <div className="space-y-3">
        {topK.map((item, index) => {
          const percentage = Math.round(item.confidence * 100);
          // Scale relative to the maximum prediction to show relative weights
          const barWidthPercent = Math.max(
            5,
            Math.round((item.confidence / maxConfidence) * 100)
          );

          return (
            <div key={item.label} className="space-y-1">
              <div className="flex justify-between text-sm font-medium">
                <span className="text-stone-700 truncate">{item.label}</span>
                <span className="text-stone-900 font-semibold">{percentage}%</span>
              </div>
              <div className="w-full h-2.5 bg-stone-100 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    index === 0
                      ? "bg-healthy-700"
                      : index === 1
                      ? "bg-healthy-500/70"
                      : "bg-stone-400/60"
                  }`}
                  style={{ width: `${barWidthPercent}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {hasClosePrediction && (
        <div className="p-3.5 bg-warning-50 border border-warning-200 text-warning-700 rounded-lg text-xs space-y-1">
          <p className="font-semibold flex items-center gap-1">
            ⚠️ Chẩn đoán cận kề
          </p>
          <p className="leading-relaxed">
            Hai nhãn dự đoán hàng đầu có độ tin cậy rất sát nhau (chênh lệch dưới 10%). 
            Khuyên dùng: Hãy đối chiếu triệu chứng thực tế trên lá cây với thông tin trong Knowledge Base 
            hoặc chụp lại ảnh cận cảnh, rõ nét hơn dưới ánh sáng tự nhiên.
          </p>
        </div>
      )}
    </div>
  );
}
