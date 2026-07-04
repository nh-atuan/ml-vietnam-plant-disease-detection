"use client";

import React from "react";
import { DiseaseRecommendation } from "../lib/api";

interface RecommendationCardProps {
  recommendation?: DiseaseRecommendation | null;
}

export default function RecommendationCard({ recommendation }: RecommendationCardProps) {
  if (!recommendation) {
    return (
      <div className="w-full p-6 bg-white border border-stone-200 rounded-xl shadow-sm text-center py-10 space-y-2">
        <p className="text-stone-500 font-medium">Chưa có khuyến nghị chuyên gia</p>
        <p className="text-xs text-stone-400 max-w-sm mx-auto">
          Mô hình không nhận diện được bệnh cụ thể hoặc nhãn này chưa có trong cơ sở tri thức chuyên gia.
        </p>
      </div>
    );
  }

  const {
    name_vi,
    name_en,
    description,
    symptoms = [],
    causes = [],
    treatments = [],
    prevention = [],
    advisory,
    sources = [],
  } = recommendation;

  return (
    <div className="w-full p-6 bg-white border border-stone-200 rounded-xl shadow-sm space-y-6">
      <div className="border-b border-stone-100 pb-3">
        <h4 className="text-sm font-semibold uppercase tracking-wider text-stone-400">
          Khuyến nghị kỹ thuật chuyên gia
        </h4>
        <h3 className="text-xl font-bold text-stone-800 mt-1">
          {name_vi}
        </h3>
        {name_en && (
          <p className="text-xs text-stone-400 italic mt-0.5">{name_en}</p>
        )}
      </div>

      {description && (
        <div className="space-y-1">
          <h5 className="text-sm font-semibold text-stone-700">Mô tả bệnh</h5>
          <p className="text-sm text-stone-600 leading-relaxed">{description}</p>
        </div>
      )}

      {symptoms.length > 0 && (
        <div className="space-y-1.5">
          <h5 className="text-sm font-semibold text-stone-700">Triệu chứng nhận biết</h5>
          <ul className="list-disc pl-5 text-sm text-stone-600 space-y-1">
            {symptoms.map((item, idx) => (
              <li key={idx} className="leading-relaxed">{item}</li>
            ))}
          </ul>
        </div>
      )}

      {causes.length > 0 && (
        <div className="space-y-1.5">
          <h5 className="text-sm font-semibold text-stone-700">Nguyên nhân dịch bệnh</h5>
          <ul className="list-disc pl-5 text-sm text-stone-600 space-y-1">
            {causes.map((item, idx) => (
              <li key={idx} className="leading-relaxed">{item}</li>
            ))}
          </ul>
        </div>
      )}

      {treatments.length > 0 && (
        <div className="space-y-1.5">
          <h5 className="text-sm font-semibold text-healthy-700 bg-healthy-50 px-2 py-1 rounded border border-healthy-100/50">
            Biện pháp xử lý & Điều trị
          </h5>
          <ul className="list-decimal pl-5 text-sm text-stone-700 space-y-1.5 font-medium">
            {treatments.map((item, idx) => (
              <li key={idx} className="leading-relaxed">{item}</li>
            ))}
          </ul>
        </div>
      )}

      {prevention.length > 0 && (
        <div className="space-y-1.5">
          <h5 className="text-sm font-semibold text-stone-700">Cách phòng ngừa chủ động</h5>
          <ul className="list-disc pl-5 text-sm text-stone-600 space-y-1">
            {prevention.map((item, idx) => (
              <li key={idx} className="leading-relaxed">{item}</li>
            ))}
          </ul>
        </div>
      )}

      {advisory && (
        <div className="p-3 border-l-4 border-warning-500 bg-warning-50/40 text-warning-700 rounded-r-lg text-xs leading-relaxed">
          <span className="font-semibold">Khuyến cáo: </span>
          {advisory}
        </div>
      )}

      {sources.length > 0 && (
        <div className="pt-4 border-t border-stone-100 space-y-1.5">
          <h5 className="text-xs font-semibold text-stone-400 uppercase tracking-wider">
            Nguồn tài liệu tham khảo
          </h5>
          <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs">
            {sources.map((src, idx) => (
              <a
                key={idx}
                href={src.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-healthy-700 hover:text-healthy-500 hover:underline transition-colors font-medium"
              >
                {src.title}
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
