"use client";

import React, { useEffect, useState } from "react";
import { fetchKnowledgeList, DiseaseRecommendation } from "../lib/api";
import LoadingSpinner from "./ui/LoadingSpinner";
import ErrorMessage from "./ui/ErrorMessage";
import EmptyState from "./ui/EmptyState";

interface KnowledgeListProps {
  onSelectDisease: (label: string) => void;
}

export default function KnowledgeList({ onSelectDisease }: KnowledgeListProps) {
  const [diseases, setDiseases] = useState<DiseaseRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadKnowledgeList = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await fetchKnowledgeList();
      setDiseases(res.items || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Không thể kết nối với cơ sở tri thức.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadKnowledgeList();
  }, []);

  if (isLoading) {
    return (
      <div className="bg-white border border-stone-200 rounded-xl p-8 shadow-sm">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <ErrorMessage
        message={error}
        onRetry={loadKnowledgeList}
      />
    );
  }

  if (diseases.length === 0) {
    return (
      <EmptyState
        title="Cơ sở tri thức trống"
        description="Không tìm thấy thông tin bệnh cây nào trong cơ sở tri thức hiện tại."
      />
    );
  }

  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-lg font-bold text-stone-850">Cơ sở tri thức bệnh cây</h3>
        <p className="text-xs text-stone-500 mt-0.5">
          Danh sách các loại bệnh trên lúa và cà phê được hệ thống hỗ trợ chẩn đoán
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {diseases.map((disease) => {
          const { label, name_vi, name_en, crop, severity, description } = disease;

          return (
            <div
              key={label}
              onClick={() => label && onSelectDisease(label)}
              className="p-5 bg-white border border-stone-200 rounded-xl hover:border-healthy-500 hover:shadow-md cursor-pointer transition-all duration-200 space-y-3 flex flex-col justify-between"
            >
              <div className="space-y-1">
                <div className="flex justify-between items-start gap-2">
                  <h4 className="font-bold text-stone-900 leading-snug">
                    {name_vi}
                  </h4>
                </div>
                {name_en && (
                  <p className="text-xs text-stone-400 italic">{name_en}</p>
                )}
                {description && (
                  <p className="text-xs text-stone-600 line-clamp-2 mt-1.5 leading-relaxed">
                    {description}
                  </p>
                )}
              </div>

              <div className="flex gap-2 pt-2 border-t border-stone-50">
                <span className="text-[10px] px-2 py-0.5 bg-healthy-50 text-healthy-700 font-semibold rounded-full border border-healthy-100/50">
                  {crop === "rice" ? "Lúa" : crop === "coffee" ? "Cà phê" : crop}
                </span>
                {severity && (
                  <span className={`text-[10px] px-2 py-0.5 font-semibold rounded-full border ${
                    severity.toLowerCase() === "high" || severity.toLowerCase() === "severe"
                      ? "bg-danger-50 text-danger-700 border-danger-100/50"
                      : severity.toLowerCase() === "medium" || severity.toLowerCase() === "moderate"
                      ? "bg-warning-50 text-warning-700 border-warning-100/50"
                      : "bg-healthy-50 text-healthy-700 border-healthy-100/50"
                  }`}>
                    {severity === "high" || severity === "severe" ? "Nặng" : severity === "medium" || severity === "moderate" ? "Trung bình" : "Nhẹ"}
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
