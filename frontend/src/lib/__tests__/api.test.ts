import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  predictImage,
  registerUser,
  loginUser,
  getCurrentUser,
  fetchHistory,
  fetchKnowledgeList,
  fetchKnowledgeDetail,
} from "../api";
import { API_BASE_URL } from "../constants";

describe("API Client tests", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("predictImage sends FormData and handles success response", async () => {
    const mockFile = new File(["dummy content"], "leaf.png", { type: "image/png" });
    const mockResponse = {
      prediction: "Healthy",
      confidence: 0.95,
      top_k: [{ label: "Healthy", confidence: 0.95 }],
      image_id: "img123",
      image_url: "http://localhost:9000/leaf.png",
      prediction_id: "pred123",
      latency_ms: 12.3,
    };

    const fetchSpy = vi.spyOn(global, "fetch").mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const result = await predictImage(mockFile);

    expect(fetchSpy).toHaveBeenCalledWith(`${API_BASE_URL}/predict`, expect.any(Object));
    const callArgs = fetchSpy.mock.calls[0];
    const fetchOptions = callArgs[1] as RequestInit;
    
    expect(fetchOptions.method).toBe("POST");
    expect(fetchOptions.body).toBeInstanceOf(FormData);
    expect(result).toEqual(mockResponse);
  });

  it("predictImage includes Authorization header when token is provided", async () => {
    const mockFile = new File(["dummy content"], "leaf.png", { type: "image/png" });
    const token = "my-secret-token";

    const fetchSpy = vi.spyOn(global, "fetch").mockResolvedValueOnce({
      ok: true,
      json: async () => ({ prediction: "Healthy" }),
    } as Response);

    await predictImage(mockFile, token);

    const fetchOptions = fetchSpy.mock.calls[0][1] as RequestInit;
    const headers = fetchOptions.headers as Record<string, string>;
    expect(headers["Authorization"]).toBe("Bearer my-secret-token");
  });

  it("predictImage handles backend detail error messages correctly", async () => {
    const mockFile = new File(["dummy content"], "leaf.png", { type: "image/png" });
    const errorDetail = "File is too large";

    vi.spyOn(global, "fetch").mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: errorDetail }),
    } as Response);

    await expect(predictImage(mockFile)).rejects.toThrow(errorDetail);
  });

  it("registerUser sends correct JSON body and returns response", async () => {
    const payload = { username: "user1", email: "user1@test.com", password: "password123" };
    const mockResponse = { id: "user-id-123", username: "user1", email: "user1@test.com", is_active: true, created_at: "2026-07-04" };

    const fetchSpy = vi.spyOn(global, "fetch").mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const result = await registerUser(payload);

    expect(fetchSpy).toHaveBeenCalledWith(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    expect(result).toEqual(mockResponse);
  });

  it("loginUser sends correct JSON body and returns TokenResponse", async () => {
    const payload = { username: "user1", password: "password123" };
    const mockResponse = { access_token: "token123", token_type: "bearer" };

    const fetchSpy = vi.spyOn(global, "fetch").mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const result = await loginUser(payload);

    expect(fetchSpy).toHaveBeenCalledWith(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    expect(result).toEqual(mockResponse);
  });

  it("getCurrentUser sets correct headers", async () => {
    const token = "token123";
    const mockResponse = { id: "uid", username: "user1", email: "user1@test.com", is_active: true, created_at: "2026" };

    const fetchSpy = vi.spyOn(global, "fetch").mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const result = await getCurrentUser(token);

    expect(fetchSpy).toHaveBeenCalledWith(`${API_BASE_URL}/auth/me`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });
    expect(result).toEqual(mockResponse);
  });

  it("fetchHistory maps query parameters correctly", async () => {
    const token = "token123";
    const mockResponse = { items: [], total: 0, page: 2, page_size: 5 };

    const fetchSpy = vi.spyOn(global, "fetch").mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const result = await fetchHistory(token, 2, 5);

    expect(fetchSpy).toHaveBeenCalledWith(`${API_BASE_URL}/history?page=2&page_size=5`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });
    expect(result).toEqual(mockResponse);
  });

  it("fetchKnowledgeList returns supported diseases list", async () => {
    const mockResponse = { items: [{ name_vi: "Đạo ôn", name_en: "Blast" }], total: 1 };

    const fetchSpy = vi.spyOn(global, "fetch").mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const result = await fetchKnowledgeList();

    expect(fetchSpy).toHaveBeenCalledWith(`${API_BASE_URL}/knowledge`, {
      method: "GET",
    });
    expect(result).toEqual(mockResponse);
  });

  it("fetchKnowledgeDetail queries correct label path", async () => {
    const mockResponse = { name_vi: "Đạo ôn", name_en: "Blast" };

    const fetchSpy = vi.spyOn(global, "fetch").mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const result = await fetchKnowledgeDetail("blast");

    expect(fetchSpy).toHaveBeenCalledWith(`${API_BASE_URL}/knowledge/blast`, {
      method: "GET",
    });
    expect(result).toEqual(mockResponse);
  });
});
