"use client";

import React from "react";
import { Info } from "lucide-react";

interface EmptyStateProps {
  title: string;
  description?: string;
}

export default function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 space-y-3 text-center border border-dashed border-stone-200 bg-white rounded-xl">
      <div className="p-3 rounded-full bg-stone-50 text-stone-400">
        <Info className="w-6 h-6" />
      </div>
      <div>
        <p className="text-sm font-semibold text-stone-700">{title}</p>
        {description && (
          <p className="text-xs text-stone-400 mt-1 max-w-sm mx-auto leading-relaxed">
            {description}
          </p>
        )}
      </div>
    </div>
  );
}
