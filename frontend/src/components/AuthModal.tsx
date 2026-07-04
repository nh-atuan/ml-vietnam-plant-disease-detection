"use client";

import React, { useEffect } from "react";
import { X } from "lucide-react";
import AuthForm from "./AuthForm";
import { useAuth } from "../hooks/useAuth";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  auth: ReturnType<typeof useAuth>;
}

export default function AuthModal({ isOpen, onClose, auth }: AuthModalProps) {
  // Prevent background scrolling when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop overlay */}
      <div
        className="fixed inset-0 bg-stone-900/60 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      {/* Modal card */}
      <div className="relative w-full max-w-md bg-white border border-stone-200 rounded-2xl shadow-xl p-6 z-10 animate-scaleUp">
        <button
          type="button"
          onClick={onClose}
          className="absolute top-4 right-4 p-1 rounded-full text-stone-400 hover:text-stone-600 hover:bg-stone-50 transition-colors"
          aria-label="Đóng cửa sổ"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="mb-4">
          <h3 className="text-lg font-bold text-stone-900">
            Tài khoản người dùng
          </h3>
          <p className="text-xs text-stone-500 mt-0.5">
            Đăng nhập để lưu trữ lịch sử chẩn đoán bệnh của bạn.
          </p>
        </div>

        <AuthForm onSuccess={onClose} auth={auth} />
      </div>
    </div>
  );
}
