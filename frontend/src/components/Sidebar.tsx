"use client";

import React, { useState } from "react";
import { Plus, BookOpen, History, ChevronLeft, ChevronRight, Leaf, User as UserIcon, LogOut, LogIn, Loader2 } from "lucide-react";
import { TabId } from "./TabNav";

interface SidebarProps {
  activeTab: TabId;
  onTabChange: (tab: TabId) => void;
  user: any;
  isLoading: boolean;
  logout: () => void;
  onLoginClick: () => void;
}

export default function Sidebar({
  activeTab,
  onTabChange,
  user,
  isLoading,
  logout,
  onLoginClick,
}: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const menuItems = [
    {
      id: "knowledge" as TabId,
      label: "Cơ sở tri thức",
      description: "Tra cứu bệnh cây trồng",
      icon: BookOpen,
    },
    {
      id: "history" as TabId,
      label: "Lịch sử chẩn đoán",
      description: "Xem lại kết quả trước",
      icon: History,
    },
  ];

  // Helper to get initials for avatar
  const getInitials = (username: string) => {
    if (!username) return "?";
    return username.slice(0, 2).toUpperCase();
  };

  return (
    <>
      {/* Mobile Bottom Navigation */}
      <nav 
        className="flex lg:hidden fixed bottom-0 left-0 right-0 bg-surface-sidebar border-t border-surface-border z-40 px-4 justify-around py-2 shadow-lg"
        role="tablist"
      >
        <button
          role="tab"
          aria-selected={activeTab === "diagnosis"}
          onClick={() => onTabChange("diagnosis")}
          className={`flex flex-col items-center justify-center py-1 px-3 rounded-xl transition-all outline-none ${
            activeTab === "diagnosis"
              ? "text-claude-orange bg-interactive-active font-semibold"
              : "text-text-secondary hover:text-claude-text"
          }`}
        >
          <Plus className="w-5 h-5 mb-0.5" />
          <span className="text-[10px] tracking-wide">Chẩn đoán</span>
        </button>

        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              role="tab"
              aria-selected={isActive}
              onClick={() => onTabChange(item.id)}
              className={`flex flex-col items-center justify-center py-1 px-3 rounded-xl transition-all outline-none ${
                isActive
                  ? "text-claude-orange bg-interactive-active font-semibold"
                  : "text-text-secondary hover:text-claude-text"
              }`}
            >
              <Icon className="w-5 h-5 mb-0.5" />
              <span className="text-[10px] tracking-wide">{item.label.split(" ")[0]}</span>
            </button>
          );
        })}
      </nav>

      {/* Desktop Sidebar */}
      <aside 
        className={`hidden lg:flex flex-col h-screen fixed left-0 top-0 border-r border-surface-border bg-surface-sidebar transition-all duration-300 z-30 ${
          isCollapsed ? "w-[72px]" : "w-64"
        }`}
        aria-label="Sidebar Navigation"
      >
        {/* Logo area */}
        <div className="flex items-center justify-between p-4 h-16">
          {!isCollapsed && (
            <div className="flex items-center gap-2">
              <Leaf className="w-5 h-5 text-claude-orange fill-claude-orange/10" />
              <span className="font-serif font-bold text-foreground text-lg tracking-tight">PlantDisease AI</span>
            </div>
          )}
          {isCollapsed && (
            <Leaf className="w-5 h-5 text-claude-orange mx-auto" />
          )}
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-1.5 rounded-lg text-text-secondary hover:text-claude-text hover:bg-interactive-active transition-colors"
            aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>

        {/* Action Button: New Chat/Diagnosis */}
        <div className="px-3 mb-4">
          <button
            onClick={() => onTabChange("diagnosis")}
            className={`w-full flex items-center justify-center gap-2 py-2 px-3 rounded-lg border border-surface-border bg-surface-raised text-sm font-medium shadow-sm transition-all hover:bg-surface-hover hover:border-border-hover ${
              isCollapsed ? "p-2 rounded-full" : ""
            } ${activeTab === "diagnosis" ? "ring-2 ring-claude-orange/20 border-claude-orange/60" : ""}`}
            title="Chẩn đoán mới"
          >
            <Plus className="w-4 h-4 text-claude-orange" />
            {!isCollapsed && <span className="text-foreground">Chẩn đoán mới</span>}
          </button>
        </div>

        {/* Navigation list */}
        <nav className="flex-1 px-3 space-y-1" role="tablist">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                role="tab"
                aria-selected={isActive}
                onClick={() => onTabChange(item.id)}
                className={`w-full flex items-center gap-3 p-2 rounded-lg text-left transition-all outline-none ${
                  isActive
                    ? "bg-interactive-active text-claude-text font-medium"
                    : "text-text-secondary hover:bg-interactive-hover hover:text-claude-text"
                }`}
              >
                <Icon className={`w-4 h-4 flex-shrink-0 ${isActive ? "text-claude-orange" : "text-text-secondary"}`} />
                {!isCollapsed && (
                  <div className="min-w-0">
                    <p className="text-sm font-medium leading-none">{item.label}</p>
                  </div>
                )}
              </button>
            );
          })}
        </nav>

        {/* Auth Section at the bottom */}
        <div className="p-3 border-t border-surface-border/50">
          {isLoading ? (
            <div className="flex items-center justify-center py-2 text-claude-muted">
              <Loader2 className="w-5 h-5 animate-spin text-claude-orange" />
            </div>
          ) : user ? (
            <div className={`flex items-center gap-3 ${isCollapsed ? "justify-center" : "justify-between"} p-1.5`}>
              <div className="flex items-center gap-2.5 min-w-0">
                <div 
                  className="w-8 h-8 rounded-full bg-claude-orange/10 border border-claude-orange/20 text-claude-orange flex items-center justify-center text-xs font-bold font-serif flex-shrink-0"
                  title={user.username}
                >
                  {getInitials(user.username)}
                </div>
                {!isCollapsed && (
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-claude-text truncate leading-tight">
                      {user.username}
                    </p>
                    <p className="text-[10px] text-claude-muted font-medium mt-0.5 leading-none">
                      Thành viên Free
                    </p>
                  </div>
                )}
              </div>
              {!isCollapsed && (
                <button
                  type="button"
                  onClick={logout}
                  className="p-1 text-stone-400 hover:text-danger-700 hover:bg-danger-50 dark:hover:bg-danger-500/10 rounded-lg transition-colors"
                  title="Đăng xuất"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              )}
            </div>
          ) : (
            <button
              type="button"
              onClick={onLoginClick}
              className={`w-full flex items-center justify-center gap-2 py-2 px-3 rounded-lg border border-surface-border bg-surface-raised text-xs font-semibold shadow-sm transition-all hover:bg-surface-hover hover:border-border-hover ${
                isCollapsed ? "p-2 rounded-full" : ""
              }`}
              title="Đăng nhập"
            >
              <LogIn className="w-4 h-4 text-claude-orange" />
              {!isCollapsed && <span className="text-claude-text">Đăng nhập</span>}
            </button>
          )}
        </div>

        {/* Footer info */}
        {!isCollapsed && (
          <div className="pb-3 text-[9px] text-text-tertiary font-medium text-center">
            v1.2.0 · Claude UI
          </div>
        )}
      </aside>
    </>
  );
}
