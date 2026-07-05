"use client";

import React, { useState } from "react";
import { useAuth } from "../hooks/useAuth";

interface AuthFormProps {
  onSuccess: () => void;
  auth: ReturnType<typeof useAuth>;
}

export default function AuthForm({ onSuccess, auth }: AuthFormProps) {
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Client-side validations
    if (username.trim().length < 3) {
      setError("Tên tài khoản phải chứa ít nhất 3 ký tự.");
      return;
    }
    if (!isLoginMode && !email.includes("@")) {
      setError("Email không hợp lệ.");
      return;
    }
    if (password.length < 6) {
      setError("Mật khẩu phải chứa ít nhất 6 ký tự.");
      return;
    }

    setIsSubmitting(true);

    try {
      if (isLoginMode) {
        await auth.login(username, password);
      } else {
        await auth.register(username, email, password);
      }
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Đã xảy ra lỗi trong quá trình xác thực.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-full space-y-5">
      <div className="flex border-b border-surface-border">
        <button
          type="button"
          onClick={() => {
            setIsLoginMode(true);
            setError(null);
          }}
          className={`flex-1 pb-3 text-sm font-semibold border-b-2 text-center transition-all focus:outline-none ${
            isLoginMode
              ? "border-claude-orange text-claude-orange font-bold"
              : "border-transparent text-text-secondary hover:text-claude-text"
          }`}
        >
          Đăng nhập
        </button>
        <button
          type="button"
          onClick={() => {
            setIsLoginMode(false);
            setError(null);
          }}
          className={`flex-1 pb-3 text-sm font-semibold border-b-2 text-center transition-all focus:outline-none ${
            !isLoginMode
              ? "border-claude-orange text-claude-orange font-bold"
              : "border-transparent text-text-secondary hover:text-claude-text"
          }`}
        >
          Đăng ký
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-claude-muted uppercase tracking-wide mb-1.5">
            Tên đăng nhập
          </label>
          <input
            type="text"
            required
            placeholder="farmer_john"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            disabled={isSubmitting}
            className="w-full px-3.5 py-2 text-sm border border-surface-border rounded-xl bg-input-bg placeholder-stone-400 focus:outline-none focus:border-claude-orange focus:ring-2 focus:ring-claude-orange/10 disabled:bg-input-disabled disabled:text-text-tertiary transition-all"
          />
        </div>

        {!isLoginMode && (
          <div>
            <label className="block text-xs font-semibold text-claude-muted uppercase tracking-wide mb-1.5">
              Địa chỉ Email
            </label>
            <input
              type="email"
              required
              placeholder="john@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isSubmitting}
              className="w-full px-3.5 py-2 text-sm border border-surface-border rounded-xl bg-input-bg placeholder-stone-400 focus:outline-none focus:border-claude-orange focus:ring-2 focus:ring-claude-orange/10 disabled:bg-input-disabled disabled:text-text-tertiary transition-all"
            />
          </div>
        )}

        <div>
          <label className="block text-xs font-semibold text-claude-muted uppercase tracking-wide mb-1.5">
            Mật khẩu
          </label>
          <input
            type="password"
            required
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={isSubmitting}
            className="w-full px-3.5 py-2 text-sm border border-surface-border rounded-xl bg-input-bg placeholder-stone-400 focus:outline-none focus:border-claude-orange focus:ring-2 focus:ring-claude-orange/10 disabled:bg-input-disabled disabled:text-text-tertiary transition-all"
          />
        </div>

        {error && (
          <div className="p-3 border border-danger-500/10 bg-danger-50 text-danger-700 rounded-xl text-xs font-medium leading-relaxed animate-in fade-in duration-200">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full py-2.5 text-sm font-semibold text-white bg-claude-orange hover:bg-amber-700 disabled:bg-stone-200 disabled:text-stone-400 disabled:cursor-not-allowed rounded-xl shadow-sm transition-all focus:outline-none"
        >
          {isSubmitting ? (
            <div className="flex items-center justify-center gap-1.5">
              <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Đang xử lý...
            </div>
          ) : isLoginMode ? (
            "Đăng nhập"
          ) : (
            "Tạo tài khoản & Đăng nhập"
          )}
        </button>
      </form>
    </div>
  );
}
