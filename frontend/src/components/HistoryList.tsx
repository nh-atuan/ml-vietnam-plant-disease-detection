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

  if (!token) {
    return (
      <div className="flex flex-col items-center justify-center py-20 px-6 space-y-6 text-center bg-background/50 dark:bg-black/20 border border-surface-border rounded-3xl shadow-sm">
        <div className="p-5 rounded-full bg-claude-orange/10 text-claude-orange shadow-inner">
          <LogIn className="w-8 h-8" />
        </div>
        <div className="space-y-2">
          <p className="text-xl font-display font-bold text-foreground">Lịch sử chẩn đoán cá nhân</p>
          <p className="text-sm font-sans text-claude-muted max-w-sm mx-auto leading-relaxed">
            Hãy đăng nhập tài khoản của bạn để tự động lưu vết chẩn đoán lá cây, tra cứu lại các khuyến nghị điều trị chuyên khoa bất cứ lúc nào.
          </p>
        </div>
        <button
          type="button"
          onClick={onLoginPrompt}
          className="inline-flex items-center gap-1.5 px-4.5 py-2.5 text-xs font-semibold text-white bg-claude-orange hover:bg-amber-700 rounded-lg shadow-sm transition-all focus:outline-none"
        >
          Đăng nhập ngay
        </button>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="bg-surface-raised border border-surface-border rounded-2xl p-8 flex items-center justify-center shadow-sm">
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
        description="Bạn chưa thực hiện phiên chẩn đoán bệnh nào sau khi đăng nhập. Hãy thử tải ảnh để chẩn đoán, kết quả sẽ tự động lưu lại đây."
      />
    );
  }

  const totalPages = Math.ceil(total / PAGE_SIZE);

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <p className="text-xs text-claude-muted font-bold tracking-wider uppercase">
          Tất cả chẩn đoán ({total})
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
              className="bg-background/50 dark:bg-black/20 border border-surface-border rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-all duration-300"
            >
              {/* Item Header */}
              <div
                onClick={() => setExpandedItemId(isExpanded ? null : item.id)}
                className="p-5 flex gap-4 items-center justify-between cursor-pointer hover:bg-surface-sidebar dark:hover:bg-zinc-800/50 select-none transition-colors"
              >
                <div className="flex gap-3.5 items-center min-w-0">
                  {item.image_url ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={item.image_url}
                      alt="History Leaf"
                      className="w-12 h-12 rounded-lg object-cover bg-surface-raised border border-surface-border flex-shrink-0"
                    />
                  ) : (
                    <div className="w-12 h-12 rounded-lg bg-surface-raised border border-surface-border text-claude-muted flex items-center justify-center flex-shrink-0">
                      <FileText className="w-5 h-5" />
                    </div>
                  )}
                  <div className="min-w-0">
                    <h4 className="font-display font-bold text-foreground text-base truncate">
                      {diseaseNameVi}
                    </h4>
                    <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-claude-muted mt-1 font-medium">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {formatDate(item.created_at)}
                      </span>
                      {crop && (
                        <span className="text-[10px] px-2 py-0.5 bg-surface-border/50 text-foreground font-semibold rounded">
                          {crop === "rice" ? "Lúa" : crop === "coffee" ? "Cà phê" : crop}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="text-right hidden sm:block">
                    <div className="text-xl font-bold font-display text-claude-orange">
                      {Math.round(item.confidence * 100)}%
                    </div>
                    <div className="text-[10px] uppercase tracking-wider text-claude-muted font-medium mt-0.5">Độ tin cậy</div>
                  </div>
                  <button
                    type="button"
                    className="p-2 rounded-full text-claude-muted hover:text-foreground hover:bg-surface-border/50 transition-colors"
                  >
                    {isExpanded ? (
                      <ChevronRight className="w-4 h-4 transform rotate-90 transition-transform duration-200" />
                    ) : (
                      <ChevronRight className="w-4 h-4 transition-transform duration-200" />
                    )}
                  </button>
                </div>
              </div>

              {/* Collapsible details content */}
              {isExpanded && (
                <div className="border-t border-surface-border p-5 bg-background/30 dark:bg-black/10">
                  <RecommendationCard recommendation={item.recommendation} />
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Pagination component */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between pt-3 border-t border-surface-border text-xs text-claude-muted font-medium">
          <span>
            Trang {page} / {totalPages}
          </span>
          <div className="flex gap-1.5">
            <button
              type="button"
              onClick={handlePrevPage}
              disabled={page === 1}
              className="inline-flex items-center justify-center p-1.5 border border-surface-border bg-surface-raised hover:bg-surface-sidebar rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm focus:outline-none"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
            </button>
            <button
              type="button"
              onClick={handleNextPage}
              disabled={page === totalPages}
              className="inline-flex items-center justify-center p-1.5 border border-surface-border bg-surface-raised hover:bg-surface-sidebar rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm focus:outline-none"
            >
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
