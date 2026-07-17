import { API_BASE_URL } from "./constants";
import { notifySessionExpired, SESSION_EXPIRED_MESSAGE } from "./auth-session";

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

type ApiErrorContext = "login" | "register" | "protected" | "generic";
type ApiField = "username" | "email" | "password";

interface RequestOptions {
  context?: ApiErrorContext;
  notifyOnUnauthorized?: boolean;
  sessionToken?: string;
}

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly fieldErrors: Partial<Record<ApiField, string>>;

  constructor({
    status,
    code,
    message,
    fieldErrors = {},
  }: {
    status: number;
    code: string;
    message: string;
    fieldErrors?: Partial<Record<ApiField, string>>;
  }) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.fieldErrors = fieldErrors;
  }
}

function getValidationFieldErrors(payload: unknown): Partial<Record<ApiField, string>> {
  if (!payload || typeof payload !== "object" || !("detail" in payload) || !Array.isArray(payload.detail)) {
    return {};
  }

  const fieldErrors: Partial<Record<ApiField, string>> = {};
  for (const detail of payload.detail) {
    if (!detail || typeof detail !== "object" || !("loc" in detail) || !Array.isArray(detail.loc)) continue;

    const field: unknown = detail.loc.at(-1);
    if (field === "username" || field === "email" || field === "password") {
      fieldErrors[field] = "Dữ liệu của trường này chưa hợp lệ.";
    }
  }
  return fieldErrors;
}

function createApiError(status: number, payload: unknown, defaultMessage: string, context: ApiErrorContext) {
  const detail = payload && typeof payload === "object" && "detail" in payload && typeof payload.detail === "string"
    ? payload.detail.toLowerCase()
    : "";

  if (status === 401) {
    if (context === "login") {
      return new ApiError({
        status,
        code: "INVALID_CREDENTIALS",
        message: "Tên đăng nhập hoặc mật khẩu không chính xác.",
      });
    }
    return new ApiError({ status, code: "SESSION_EXPIRED", message: SESSION_EXPIRED_MESSAGE });
  }

  if (status === 409 && context === "register") {
    const fieldErrors: Partial<Record<ApiField, string>> = detail.includes("email")
      ? { email: "Địa chỉ email này đã được sử dụng." }
      : detail.includes("username")
        ? { username: "Tên đăng nhập này đã được sử dụng." }
        : {};
    return new ApiError({
      status,
      code: "ACCOUNT_EXISTS",
      message: "Tên đăng nhập hoặc địa chỉ email đã được sử dụng.",
      fieldErrors,
    });
  }

  if (status === 400 || status === 422) {
    return new ApiError({
      status,
      code: "VALIDATION_ERROR",
      message: "Dữ liệu nhập không hợp lệ. Vui lòng kiểm tra lại các trường bắt buộc.",
      fieldErrors: getValidationFieldErrors(payload),
    });
  }

  if (status === 413) {
    return new ApiError({
      status,
      code: "PAYLOAD_TOO_LARGE",
      message: "Tệp gửi lên vượt quá dung lượng cho phép.",
    });
  }

  if (status >= 500) {
    return new ApiError({
      status,
      code: "SERVER_ERROR",
      message: "Máy chủ đang gặp sự cố. Vui lòng thử lại sau.",
    });
  }

  return new ApiError({ status, code: "REQUEST_FAILED", message: defaultMessage });
}

async function request<T>(url: string, init: RequestInit, defaultMessage: string, options: RequestOptions = {}): Promise<T> {
  try {
    const response = await fetch(url, init);
    if (!response.ok) {
      let payload: unknown = null;
      try {
        payload = await response.json();
      } catch {
        // Keep the safe fallback instead of exposing an untrusted response body.
      }

      const error = createApiError(response.status, payload, defaultMessage, options.context ?? "generic");
      if (error.status === 401 && options.notifyOnUnauthorized && options.sessionToken) {
        notifySessionExpired(options.sessionToken);
      }
      throw error;
    }
    return response.json() as Promise<T>;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError({
      status: 0,
      code: "NETWORK_ERROR",
      message: "Không thể kết nối máy chủ. Vui lòng kiểm tra mạng và thử lại.",
    });
  }
}

export async function predictImage(file: File, token?: string): Promise<PredictionResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const headers: HeadersInit = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  return request<PredictionResponse>(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers,
    body: formData,
  }, "Không thể gửi ảnh để dự đoán.", {
    context: token ? "protected" : "generic",
    notifyOnUnauthorized: Boolean(token),
    sessionToken: token,
  });
}

export async function registerUser(data: UserCreate): Promise<UserResponse> {
  return request<UserResponse>(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  }, "Đăng ký không thành công.", { context: "register" });
}

export async function loginUser(data: LoginRequest): Promise<TokenResponse> {
  return request<TokenResponse>(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  }, "Đăng nhập không thành công.", { context: "login" });
}

export async function getCurrentUser(token: string, notifyOnUnauthorized = true): Promise<UserResponse> {
  return request<UserResponse>(`${API_BASE_URL}/auth/me`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  }, "Không thể lấy thông tin người dùng.", {
    context: "protected",
    notifyOnUnauthorized,
    sessionToken: token,
  });
}

export async function fetchHistory(token: string, page = 1, pageSize = 10): Promise<HistoryResponse> {
  return request<HistoryResponse>(`${API_BASE_URL}/history?page=${page}&page_size=${pageSize}`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  }, "Không thể lấy lịch sử dự đoán.", {
    context: "protected",
    notifyOnUnauthorized: true,
    sessionToken: token,
  });
}

export async function fetchKnowledgeList(): Promise<KnowledgeListResponse> {
  return request<KnowledgeListResponse>(`${API_BASE_URL}/knowledge`, {
    method: "GET",
  }, "Không thể lấy danh sách kiến thức.");
}

export async function fetchKnowledgeDetail(label: string): Promise<DiseaseRecommendation> {
  return request<DiseaseRecommendation>(`${API_BASE_URL}/knowledge/${label}`, {
    method: "GET",
  }, `Không thể lấy thông tin chi tiết của bệnh: ${label}`);
}
