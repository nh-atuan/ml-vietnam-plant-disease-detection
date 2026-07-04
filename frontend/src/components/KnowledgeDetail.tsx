"use client";

import React, { useEffect, useState } from "react";
import { ArrowLeft } from "lucide-react";
import { fetchKnowledgeDetail, DiseaseRecommendation } from "../lib/api";
import LoadingSpinner from "./ui/LoadingSpinner";
import ErrorMessage from "./ui/ErrorMessage";
import RecommendationCard from "./RecommendationCard";

interface KnowledgeDetailProps {
  diseaseLabel: string;
  onBack: () => void;
}

export default function KnowledgeDetail({ diseaseLabel, onBack }: KnowledgeDetailProps) {
  const [disease, setDisease] = useState<DiseaseRecommendation | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDiseaseDetail = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchKnowledgeDetail(diseaseLabel);
      setDisease(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Không thể lấy thông tin chi tiết về loại bệnh này.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadDiseaseDetail();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [diseaseLabel]);

  if (isLoading) {
    return (
      <div className="bg-white border border-stone-200 rounded-xl p-8 shadow-sm">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4">
        <button
          type="button"
          onClick={onBack}
          className="inline-flex items-center gap-1 text-sm font-semibold text-stone-600 hover:text-stone-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Quay lại danh sách
        </button>
        <ErrorMessage message={error} onRetry={loadDiseaseDetail} />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <button
        type="button"
        onClick={onBack}
        className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-stone-700 bg-white border border-stone-200 rounded-lg hover:bg-stone-50 hover:text-stone-900 transition-all shadow-sm focus:outline-none"
      >
        <ArrowLeft className="w-3.5 h-3.5" />
        Quay lại danh sách
      </button>

      {disease && <RecommendationCard recommendation={disease} />}
    </div>
  );
}
