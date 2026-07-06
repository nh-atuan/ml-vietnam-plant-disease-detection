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
        className="fixed inset-0 bg-stone-900/40 backdrop-blur-xs transition-opacity duration-300"
        onClick={onClose}
      />

      {/* Modal card */}
      <div className="relative w-full max-w-sm bg-surface-raised border border-surface-border rounded-xl shadow-xl p-6 z-10 animate-in fade-in zoom-in-95 duration-200">
        <button
          type="button"
          onClick={onClose}
          className="absolute top-4.5 right-4.5 p-1 rounded-lg text-claude-muted hover:text-claude-text hover:bg-surface-sidebar transition-all focus:outline-none"
          aria-label="Đóng cửa sổ"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="mb-5 space-y-1">
          <h3 className="text-base font-bold text-claude-text">
            Tài khoản Studio
          </h3>
          <p className="text-xs text-claude-muted font-medium">
            Đăng nhập để xem lịch sử chẩn đoán bệnh của bạn.
          </p>
        </div>

        <AuthForm onSuccess={onClose} auth={auth} />
      </div>
    </div>
  );
}
