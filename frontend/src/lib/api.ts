export type TopKPrediction = {
  label: string;
  confidence: number;
};

export type PredictionResponse = {
  prediction: string;
  confidence: number;
  top_k: TopKPrediction[];
  recommendation?: {
    label?: string;
    crop?: string;
    name_vi: string;
    name_en: string;
    description?: string;
    symptoms?: string[];
    causes?: string[];
    treatments: string[];
    prevention?: string[];
    severity?: string;
    sources?: Array<{
      title: string;
      url: string;
    }>;
    confidence?: number;
    confidence_note?: string;
    advisory?: string;
  };
  image_id?: string;
  image_url?: string;
};

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export async function predictImage(file: File): Promise<PredictionResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    let message = "Không thể gửi ảnh để dự đoán.";
    try {
      const payload = (await response.json()) as { detail?: string };
      message = payload.detail ?? message;
    } catch {
      // Keep the generic message when the API does not return JSON.
    }
    throw new Error(message);
  }

  return (await response.json()) as PredictionResponse;
}
