"use client";

import React, { useEffect, useState } from "react";
import { LogIn, Calendar, FileText, ChevronLeft, ChevronRight } from "lucide-react";
import { fetchHistory, HistoryItem } from "../lib/api";
import LoadingSpinner from "./ui/LoadingSpinner";
import ErrorMessage from "./ui/ErrorMessage";
import EmptyState from "./ui/EmptyState";
import RecommendationCard from "./RecommendationCard";

interface HistoryListProps {
  token: string | null;
  onLoginPrompt: () => void;
}

export default function HistoryList({ token, onLoginPrompt }: HistoryListProps) {
  const [historyItems, setHistoryItems] = useState<HistoryItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedItemId, setExpandedItemId] = useState<string | null>(null);

  const PAGE_SIZE = 5;

  const loadHistory = async (targetPage = page) => {
    if (!token) return;
    setIsLoading(true);
    setError(null);
    try {
      const res = await fetchHistory(token, targetPage, PAGE_SIZE);
      setHistoryItems(res.items || []);
      setTotal(res.total || 0);
      setPage(res.page || targetPage);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Không thể lấy lịch sử chẩn đoán.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      loadHistory(1);
    } else {
      setHistoryItems([]);
      setTotal(0);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const handlePrevPage = () => {
    if (page > 1) {
      loadHistory(page - 1);
    }
  };

  const handleNextPage = () => {
    if (page * PAGE_SIZE < total) {
      loadHistory(page + 1);
    }
  };

  const formatDate = (dateStr: string) => {
    try {
      const date = new Date(dateStr);
      return date.toLocaleString("vi-VN", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return dateStr;
    }
  };

  // If user is not logged in
  if (!token) {
    return (
      <div className="flex flex-col items-center justify-center py-16 px-4 space-y-4 text-center border border-dashed border-stone-200 bg-white rounded-xl">
        <div className="p-3 rounded-full bg-healthy-50 text-healthy-700">
          <LogIn className="w-6 h-6" />
        </div>
        <div className="space-y-1">
          <p className="text-sm font-semibold text-stone-700">Lịch sử chẩn đoán cá nhân</p>
          <p className="text-xs text-stone-400 max-w-xs mx-auto leading-relaxed">
            Đăng nhập để tự động lưu vết các lần chẩn đoán lá cây và xem lại khuyến nghị bất cứ lúc nào.
          </p>
        </div>
        <button
          type="button"
          onClick={onLoginPrompt}
          className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-white bg-healthy-700 hover:bg-healthy-500 rounded-lg shadow-sm transition-all"
        >
          Đăng nhập ngay
        </button>
      </div>
    );
  }

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
        onRetry={() => loadHistory(page)}
      />
    );
  }

  if (historyItems.length === 0) {
    return (
      <EmptyState
        title="Lịch sử chẩn đoán trống"
        description="Bạn chưa thực hiện cuộc chẩn đoán nào khi đang đăng nhập. Kết quả sẽ tự động lưu sau khi bạn chụp/gửi ảnh chẩn đoán."
      />
    );
  }

  const totalPages = Math.ceil(total / PAGE_SIZE);

  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-lg font-bold text-stone-850">Lịch sử chẩn đoán của bạn</h3>
        <p className="text-xs text-stone-500 mt-0.5">
          Hiển thị tổng số {total} lần chẩn đoán đã lưu
        </p>
      </div>

      <div className="space-y-3">
        {historyItems.map((item) => {
          const isExpanded = expandedItemId === item.id;
          const diseaseNameVi = item.recommendation?.name_vi || item.predicted_label;
          const crop = item.recommendation?.crop;

          return (
            <div
              key={item.id}
              className="bg-white border border-stone-200 rounded-xl overflow-hidden shadow-sm transition-all duration-200"
            >
              {/* Item Summary Header */}
              <div
                onClick={() => setExpandedItemId(isExpanded ? null : item.id)}
                className="p-4 flex gap-4 items-center justify-between cursor-pointer hover:bg-stone-50/50 select-none"
              >
                <div className="flex gap-3 items-center min-w-0">
                  {item.image_url ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={item.image_url}
                      alt="History leaf thumbnail"
                      className="w-12 h-12 rounded-lg object-cover bg-stone-100 flex-shrink-0"
                    />
                  ) : (
                    <div className="w-12 h-12 rounded-lg bg-stone-100 text-stone-400 flex items-center justify-center flex-shrink-0">
                      <FileText className="w-6 h-6" />
                    </div>
                  )}
                  <div className="min-w-0">
                    <h4 className="font-bold text-stone-850 text-sm truncate">
                      {diseaseNameVi}
                    </h4>
                    <div className="flex flex-wrap items-center gap-x-2 gap-y-0.5 text-xs text-stone-450 mt-0.5">
                      <span className="flex items-center gap-0.5">
                        <Calendar className="w-3.5 h-3.5" />
                        {formatDate(item.created_at)}
                      </span>
                      {crop && (
                        <span className="text-[10px] px-1.5 py-0.2 bg-stone-100 text-stone-600 rounded">
                          {crop === "rice" ? "Lúa" : crop === "coffee" ? "Cà phê" : crop}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <div className="text-sm font-bold text-healthy-700">
                      {Math.round(item.confidence * 100)}%
                    </div>
                    <div className="text-[10px] text-stone-400">Độ tin cậy</div>
                  </div>
                  <button
                    type="button"
                    className="p-1 rounded text-stone-400 hover:text-stone-600 transition-colors"
                  >
                    {isExpanded ? (
                      <ChevronRight className="w-4 h-4 transform rotate-90 transition-transform" />
                    ) : (
                      <ChevronRight className="w-4 h-4 transition-transform" />
                    )}
                  </button>
                </div>
              </div>

              {/* Expanded Expert Recommendations */}
              {isExpanded && (
                <div className="border-t border-stone-100 p-4 bg-stone-50/30">
                  <RecommendationCard recommendation={item.recommendation} />
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between pt-2 border-t border-stone-100 text-sm">
          <span className="text-xs text-stone-500">
            Trang {page} / {totalPages}
          </span>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={handlePrevPage}
              disabled={page === 1}
              className="inline-flex items-center justify-center p-1.5 border border-stone-200 bg-white hover:bg-stone-50 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              type="button"
              onClick={handleNextPage}
              disabled={page === totalPages}
              className="inline-flex items-center justify-center p-1.5 border border-stone-200 bg-white hover:bg-stone-50 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
