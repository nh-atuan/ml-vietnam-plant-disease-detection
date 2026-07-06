"use client";

import { useState, useEffect, useCallback } from "react";
import { loginUser, registerUser, getCurrentUser, UserResponse } from "../lib/api";

const TOKEN_KEY = "plant_disease_token";

export function useAuth() {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Restore token and user on mount
  useEffect(() => {
    async function restoreSession() {
      const storedToken = localStorage.getItem(TOKEN_KEY);
      if (storedToken) {
        try {
          const userData = await getCurrentUser(storedToken);
          setToken(storedToken);
          setUser(userData);
        } catch (err) {
          console.error("Failed to restore session:", err);
          localStorage.removeItem(TOKEN_KEY);
        }
      }
      setIsLoading(false);
    }
    restoreSession();
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    setIsLoading(true);
    try {
      const loginRes = await loginUser({ username, password });
      localStorage.setItem(TOKEN_KEY, loginRes.access_token);
      setToken(loginRes.access_token);
      
      const userData = await getCurrentUser(loginRes.access_token);
      setUser(userData);
    } catch (err) {
      localStorage.removeItem(TOKEN_KEY);
      setToken(null);
      setUser(null);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const register = useCallback(async (username: string, email: string, password: string) => {
    setIsLoading(true);
    try {
      await registerUser({ username, email, password });
      // Automatically login after successful registration
      const loginRes = await loginUser({ username, password });
      localStorage.setItem(TOKEN_KEY, loginRes.access_token);
      setToken(loginRes.access_token);
      
      const userData = await getCurrentUser(loginRes.access_token);
      setUser(userData);
    } catch (err) {
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setUser(null);
  }, []);

  return {
    user,
    token,
    isLoading,
    login,
    register,
    logout,
  };
}
export type UseAuthReturn = ReturnType<typeof useAuth>;
