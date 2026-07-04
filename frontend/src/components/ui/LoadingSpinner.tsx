"use client";

import React from "react";

export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 space-y-3 text-center">
      <div className="relative w-10 h-10">
        <div className="absolute top-0 left-0 w-full h-full border-4 border-stone-100 rounded-full"></div>
        <div className="absolute top-0 left-0 w-full h-full border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
      <p className="text-sm font-semibold text-stone-700">Đang xử lý phân tích...</p>
      <p className="text-xs text-stone-500">Mô hình AI đang chẩn đoán hình ảnh lá cây</p>
    </div>
  );
}
