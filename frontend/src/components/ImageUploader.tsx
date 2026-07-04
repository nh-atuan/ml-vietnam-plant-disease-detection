"use client";

import React, { useRef, useState } from "react";
import { Upload, Camera, X } from "lucide-react";
import { ALLOWED_IMAGE_TYPES, MAX_FILE_SIZE_BYTES } from "../lib/constants";

interface ImageUploaderProps {
  selectedFile: File | null;
  onFileSelect: (file: File | null, validationError: string | null) => void;
  isSubmitting: boolean;
  onSubmit: () => void;
  error: string | null;
}

export default function ImageUploader({
  selectedFile,
  onFileSelect,
  isSubmitting,
  onSubmit,
  error,
}: ImageUploaderProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const [isDragActive, setIsDragActive] = useState(false);

  const validateAndSelectFile = (file: File | null) => {
    if (!file) {
      onFileSelect(null, null);
      return;
    }

    if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
      onFileSelect(null, "Chỉ hỗ trợ các định dạng ảnh JPEG, PNG hoặc WEBP.");
      return;
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      onFileSelect(null, "Kích thước ảnh vượt quá giới hạn 10 MB.");
      return;
    }

    onFileSelect(file, null);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    validateAndSelectFile(file);
    // Reset inputs so the same file can be selected again if reset
    if (e.target) e.target.value = "";
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragActive(true);
    } else if (e.type === "dragleave") {
      setIsDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    const file = e.dataTransfer.files?.[0] || null;
    validateAndSelectFile(file);
  };

  const triggerFileSelect = () => {
    fileInputRef.current?.click();
  };

  const triggerCameraSelect = () => {
    cameraInputRef.current?.click();
  };

  const handleReset = (e: React.MouseEvent) => {
    e.stopPropagation(); // Avoid triggering label click if nested
    onFileSelect(null, null);
  };

  // Helper to format file size
  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  // Create preview URL if file exists
  const previewUrl = selectedFile ? URL.createObjectURL(selectedFile) : null;

  return (
    <div className="w-full space-y-4">
      <div
        className={`relative flex flex-col items-center justify-center min-h-[320px] p-6 border-2 border-dashed rounded-xl transition-all duration-200 ${
          isDragActive
            ? "border-emerald-500 bg-emerald-50/50"
            : "border-stone-200 bg-stone-50/50 hover:bg-stone-50"
        } ${selectedFile ? "border-solid bg-white" : ""}`}
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
      >
        {selectedFile && previewUrl ? (
          <div className="relative w-full flex flex-col items-center gap-4">
            <div className="relative w-full max-h-[260px] flex justify-center items-center overflow-hidden rounded-lg bg-stone-100">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={previewUrl}
                alt="Leaf preview"
                className="max-w-full max-h-[260px] object-contain transition-transform duration-200 hover:scale-[1.02]"
              />
              <button
                type="button"
                onClick={handleReset}
                className="absolute top-2 right-2 p-1.5 rounded-full bg-stone-900/80 text-white hover:bg-stone-900 transition-colors focus:ring-2 focus:ring-healthy-500 focus:outline-none"
                aria-label="Hủy chọn ảnh"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="w-full text-center px-4">
              <p className="text-sm font-semibold text-stone-800 truncate" title={selectedFile.name}>
                {selectedFile.name}
              </p>
              <p className="text-xs text-stone-500 mt-0.5">
                {formatFileSize(selectedFile.size)}
              </p>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center text-center gap-4 py-8">
            <div className="p-4 rounded-full bg-healthy-50 text-healthy-700">
              <Upload className="w-8 h-8" />
            </div>
            <div>
              <p className="text-base font-semibold text-stone-800">
                Kéo thả hoặc chọn ảnh lá cây để chẩn đoán
              </p>
              <p className="text-xs text-stone-500 mt-1">
                Hỗ trợ PNG, JPG, WEBP lên đến 10 MB
              </p>
            </div>
            <div className="flex flex-wrap gap-2 justify-center">
              <button
                type="button"
                onClick={triggerFileSelect}
                className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-stone-700 bg-white border border-stone-200 rounded-lg hover:bg-stone-50 hover:text-stone-900 transition-all shadow-sm focus:outline-none focus:ring-2 focus:ring-healthy-500"
              >
                <Upload className="w-4 h-4" />
                Chọn file ảnh
              </button>
              <button
                type="button"
                onClick={triggerCameraSelect}
                className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-stone-700 bg-white border border-stone-200 rounded-lg hover:bg-stone-50 hover:text-stone-900 transition-all shadow-sm focus:outline-none focus:ring-2 focus:ring-healthy-500"
              >
                <Camera className="w-4 h-4" />
                Chụp ảnh
              </button>
            </div>
          </div>
        )}

        {/* Hidden inputs */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/png,image/jpeg,image/webp"
          className="hidden"
          onChange={handleFileChange}
        />
        <input
          ref={cameraInputRef}
          type="file"
          accept="image/png,image/jpeg,image/webp"
          capture="environment"
          className="hidden"
          onChange={handleFileChange}
        />
      </div>

      <button
        type="button"
        onClick={onSubmit}
        disabled={isSubmitting || !selectedFile}
        className="w-full inline-flex items-center justify-center px-4 py-3 text-sm font-semibold text-white bg-healthy-700 hover:bg-healthy-500 rounded-lg shadow-sm disabled:bg-stone-300 disabled:text-stone-500 disabled:cursor-not-allowed transition-all focus:outline-none focus:ring-2 focus:ring-healthy-500 focus:ring-offset-2"
      >
        {isSubmitting ? "Đang xử lý chẩn đoán..." : "Gửi ảnh để chẩn đoán"}
      </button>

      {error && (
        <div className="p-3 border border-danger-500/10 bg-danger-50 text-danger-700 rounded-lg text-sm flex gap-2 items-start animate-fadeIn">
          <span className="font-semibold">Lỗi:</span>
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
