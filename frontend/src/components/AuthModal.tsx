"use client";

import React from "react";
import AuthForm from "./AuthForm";
import { useAuth } from "../hooks/useAuth";
import { Dialog, DialogContent } from "./ui/Dialog";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  auth: ReturnType<typeof useAuth>;
}

export default function AuthModal({ isOpen, onClose, auth }: AuthModalProps) {
  return (
    <Dialog open={isOpen} onClose={onClose}>
      <DialogContent
        title="Tài khoản PlantDisease AI"
        description="Đăng nhập để lưu và xem lại lịch sử chẩn đoán của bạn."
      >
        <AuthForm onSuccess={onClose} auth={auth} />
      </DialogContent>
    </Dialog>
  );
}
