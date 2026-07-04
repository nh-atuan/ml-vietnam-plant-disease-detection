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

    setIsSubmitting(false);
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
    <div className="w-full space-y-4">
      <div className="flex border-b border-stone-200">
        <button
          type="button"
          onClick={() => {
            setIsLoginMode(true);
            setError(null);
          }}
          className={`flex-1 pb-2.5 text-sm font-semibold border-b-2 text-center transition-all ${
            isLoginMode
              ? "border-healthy-700 text-healthy-700 font-bold"
              : "border-transparent text-stone-500 hover:text-stone-700"
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
          className={`flex-1 pb-2.5 text-sm font-semibold border-b-2 text-center transition-all ${
            !isLoginMode
              ? "border-healthy-700 text-healthy-700 font-bold"
              : "border-transparent text-stone-500 hover:text-stone-700"
          }`}
        >
          Đăng ký
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-stone-600 uppercase mb-1">
            Tên đăng nhập
          </label>
          <input
            type="text"
            required
            placeholder="farmer_john"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            disabled={isSubmitting}
            className="w-full px-3 py-2 text-sm border border-stone-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-healthy-500 focus:border-transparent disabled:bg-stone-50 disabled:text-stone-400"
          />
        </div>

        {!isLoginMode && (
          <div>
            <label className="block text-xs font-semibold text-stone-600 uppercase mb-1">
              Địa chỉ Email
            </label>
            <input
              type="email"
              required
              placeholder="john@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isSubmitting}
              className="w-full px-3 py-2 text-sm border border-stone-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-healthy-500 focus:border-transparent disabled:bg-stone-50 disabled:text-stone-400"
            />
          </div>
        )}

        <div>
          <label className="block text-xs font-semibold text-stone-600 uppercase mb-1">
            Mật khẩu
          </label>
          <input
            type="password"
            required
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={isSubmitting}
            className="w-full px-3 py-2 text-sm border border-stone-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-healthy-500 focus:border-transparent disabled:bg-stone-50 disabled:text-stone-400"
          />
        </div>

        {error && (
          <div className="p-3 text-xs border border-danger-500/20 bg-danger-50 text-danger-700 rounded-lg">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full py-2.5 text-sm font-semibold text-white bg-healthy-700 hover:bg-healthy-500 rounded-lg shadow-sm disabled:bg-stone-300 disabled:cursor-not-allowed transition-all focus:outline-none focus:ring-2 focus:ring-healthy-500"
        >
          {isSubmitting
            ? "Đang xử lý..."
            : isLoginMode
            ? "Đăng nhập"
            : "Tạo tài khoản & Đăng nhập"}
        </button>
      </form>
    </div>
  );
}
