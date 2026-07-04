"use client";

import React from "react";
import { AlertCircle, RefreshCw } from "lucide-react";

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export default function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  return (
    <div className="flex flex-col items-center justify-center p-6 border border-red-200 bg-red-50/50 rounded-xl space-y-4 text-center max-w-lg mx-auto">
      <div className="p-3 rounded-full bg-red-100 text-red-600">
        <AlertCircle className="w-6 h-6" />
      </div>
      <div className="space-y-1">
        <p className="text-sm font-bold text-red-800">Không thể thực hiện tác vụ</p>
        <p className="text-xs text-red-700 leading-relaxed">{message}</p>
      </div>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-red-800 bg-red-100 hover:bg-red-200 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-red-500"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Thử lại
        </button>
      )}
    </div>
  );
}
