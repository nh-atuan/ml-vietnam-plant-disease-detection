"use client";

import React, { useState } from "react";
import { User, LogIn, LogOut, Loader2 } from "lucide-react";
import ImageUploader from "../components/ImageUploader";
import PredictionResult from "../components/PredictionResult";
import TopKList from "../components/TopKList";
import RecommendationCard from "../components/RecommendationCard";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import EmptyState from "../components/ui/EmptyState";
import TabNav, { TabId } from "../components/TabNav";
import AuthModal from "../components/AuthModal";
import KnowledgeList from "../components/KnowledgeList";
import KnowledgeDetail from "../components/KnowledgeDetail";
import HistoryList from "../components/HistoryList";
import { usePrediction } from "../hooks/usePrediction";
import { useAuth } from "../hooks/useAuth";

export default function Home() {
  const auth = useAuth();
  const {
    selectedFile,
    prediction,
    error,
    isSubmitting,
    handleFileSelect,
    handleSubmit,
  } = usePrediction();

  const [activeTab, setActiveTab] = useState<TabId>("diagnosis");
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [selectedDisease, setSelectedDisease] = useState<string | null>(null);

  const handlePredictSubmit = () => {
    // Pass auth token if available to associate with history
    handleSubmit(auth.token || undefined);
  };

  return (
    <main className="min-h-screen px-4 py-6 sm:px-8 bg-[#f7f9f6]">
      <section className="mx-auto flex w-full max-w-5xl flex-col gap-6">
        
        {/* Header Title Block & Auth Area */}
        <div className="flex flex-col gap-4 border-b border-stone-200 pb-4">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
            <div className="space-y-1">
              <p className="text-sm font-medium uppercase tracking-wider text-healthy-700">
                Cà phê / Lúa
              </p>
              <h1 className="text-3xl font-bold text-stone-900 sm:text-4xl">
                Chẩn đoán bệnh trên lá cây
              </h1>
              <p className="max-w-2xl text-xs text-stone-500">
                Dự đoán và nhận khuyến nghị điều trị cho bệnh trên lá cây lúa và cà phê 
                trong điều kiện thực địa tại Việt Nam.
              </p>
            </div>

            {/* Auth Section */}
            <div className="flex items-center self-start sm:self-center">
              {auth.isLoading ? (
                <div className="flex items-center gap-1.5 text-xs text-stone-400 bg-white border border-stone-100 px-3 py-1.5 rounded-lg">
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  Đang xác thực...
                </div>
              ) : auth.user ? (
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-1.5 text-xs text-stone-750 bg-white border border-stone-200 px-3 py-1.5 rounded-lg shadow-sm">
                    <User className="w-3.5 h-3.5 text-healthy-700" />
                    <span className="font-semibold">{auth.user.username}</span>
                  </div>
                  <button
                    type="button"
                    onClick={auth.logout}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-stone-600 hover:text-danger-700 bg-white hover:bg-danger-50 border border-stone-200 hover:border-danger-200 rounded-lg transition-all shadow-sm focus:outline-none"
                  >
                    <LogOut className="w-3.5 h-3.5" />
                    Đăng xuất
                  </button>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={() => setIsAuthModalOpen(true)}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-stone-700 bg-white border border-stone-200 hover:bg-stone-50 hover:text-stone-900 rounded-lg transition-all shadow-sm focus:outline-none"
                >
                  <LogIn className="w-3.5 h-3.5 text-healthy-700" />
                  Đăng nhập
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <TabNav activeTab={activeTab} onTabChange={setActiveTab} />

        {/* Tab Panels */}
        <div className="mt-2">
          {/* TAB 1: DIAGNOSIS */}
          {activeTab === "diagnosis" && (
            <div className="grid gap-6 lg:grid-cols-[1fr_1fr] items-start">
              {/* Left Column: Upload */}
              <div className="space-y-4">
                <h2 className="text-lg font-bold text-stone-850">Tải ảnh lên</h2>
                <ImageUploader
                  selectedFile={selectedFile}
                  onFileSelect={handleFileSelect}
                  isSubmitting={isSubmitting}
                  onSubmit={handlePredictSubmit}
                  error={error}
                />
              </div>

              {/* Right Column: Result */}
              <div className="space-y-4">
                <h2 className="text-lg font-bold text-stone-850">Kết quả chẩn đoán</h2>
                
                {isSubmitting && (
                  <div className="bg-white border border-stone-200 rounded-xl p-6 shadow-sm">
                    <LoadingSpinner />
                  </div>
                )}

                {!isSubmitting && !prediction && (
                  <EmptyState
                    title="Chưa có dữ liệu chẩn đoán"
                    description="Hãy chọn hoặc chụp ảnh một chiếc lá cây (lúa hoặc cà phê) bên cột trái để bắt đầu phân tích bệnh."
                  />
                )}

                {!isSubmitting && prediction && (
                  <div className="space-y-4">
                    <PredictionResult prediction={prediction} />
                    <TopKList topK={prediction.top_k} />
                    <RecommendationCard recommendation={prediction.recommendation} />
                  </div>
                )}
              </div>
            </div>
          )}

          {/* TAB 2: KNOWLEDGE BASE */}
          {activeTab === "knowledge" && (
            <div>
              {selectedDisease ? (
                <KnowledgeDetail
                  diseaseLabel={selectedDisease}
                  onBack={() => setSelectedDisease(null)}
                />
              ) : (
                <KnowledgeList onSelectDisease={setSelectedDisease} />
              )}
            </div>
          )}

          {/* TAB 3: PERSONAL HISTORY */}
          {activeTab === "history" && (
            <HistoryList
              token={auth.token}
              onLoginPrompt={() => setIsAuthModalOpen(true)}
            />
          )}
        </div>

      </section>

      {/* Auth Modal Overlay */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        auth={auth}
      />
    </main>
  );
}
