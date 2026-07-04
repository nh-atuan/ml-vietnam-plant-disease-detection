import { API_BASE_URL } from "./constants";

export type TopKPrediction = {
  label: string;
  confidence: number;
};

export type KnowledgeSource = {
  title: string;
  url: string;
};

export type DiseaseRecommendation = {
  label?: string;
  crop?: string;
  name_vi: string;
  name_en: string;
  description?: string;
  symptoms: string[];
  causes: string[];
  treatments: string[];
  prevention: string[];
  severity?: string;
  sources: KnowledgeSource[];
  confidence?: number;
  confidence_note?: string;
  advisory?: string;
};

export type PredictionResponse = {
  prediction: string;
  confidence: number;
  top_k: TopKPrediction[];
  recommendation?: DiseaseRecommendation;
  image_id?: string;
  image_url?: string;
  prediction_id?: string;
  latency_ms?: number;
};

export type UserCreate = {
  username: string;
  email: string;
  password: string;
};

export type UserResponse = {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
};

export type LoginRequest = {
  username: string;
  password: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
};

export type HistoryItem = {
  id: string;
  image_id: string;
  predicted_label: string;
  confidence: number;
  top_k: TopKPrediction[];
  recommendation?: DiseaseRecommendation;
  image_url?: string;
  created_at: string;
};

export type HistoryResponse = {
  items: HistoryItem[];
  total: number;
  page: number;
  page_size: number;
};

export type KnowledgeListResponse = {
  items: DiseaseRecommendation[];
  total: number;
};

// Helper for consistent API error parsing
async function handleResponse(response: Response, defaultMessage: string): Promise<any> {
  if (!response.ok) {
    let message = defaultMessage;
    try {
      const payload = await response.json();
      if (payload && typeof payload.detail === "string") {
        message = payload.detail;
      } else if (payload && Array.isArray(payload.detail)) {
        // Validation errors
        message = payload.detail.map((err: any) => err.msg || JSON.stringify(err)).join(", ");
      }
    } catch {
      // Keep default message if not JSON
    }
    throw new Error(message);
  }
  return response.json();
}

export async function predictImage(file: File, token?: string): Promise<PredictionResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const headers: HeadersInit = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers,
    body: formData,
  });

  return handleResponse(response, "Không thể gửi ảnh để dự đoán.");
}

export async function registerUser(data: UserCreate): Promise<UserResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return handleResponse(response, "Đăng ký không thành công.");
}

export async function loginUser(data: LoginRequest): Promise<TokenResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return handleResponse(response, "Đăng nhập không thành công.");
}

export async function getCurrentUser(token: string): Promise<UserResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });

  return handleResponse(response, "Không thể lấy thông tin người dùng.");
}

export async function fetchHistory(token: string, page = 1, pageSize = 10): Promise<HistoryResponse> {
  const response = await fetch(`${API_BASE_URL}/history?page=${page}&page_size=${pageSize}`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });

  return handleResponse(response, "Không thể lấy lịch sử dự đoán.");
}

export async function fetchKnowledgeList(): Promise<KnowledgeListResponse> {
  const response = await fetch(`${API_BASE_URL}/knowledge`, {
    method: "GET",
  });

  return handleResponse(response, "Không thể lấy danh sách kiến thức.");
}

export async function fetchKnowledgeDetail(label: string): Promise<DiseaseRecommendation> {
  const response = await fetch(`${API_BASE_URL}/knowledge/${label}`, {
    method: "GET",
  });

  return handleResponse(response, `Không thể lấy thông tin chi tiết của bệnh: ${label}`);
}
