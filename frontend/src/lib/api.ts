export type TopKPrediction = {
  label: string;
  confidence: number;
};

export type PredictionResponse = {
  prediction: string;
  confidence: number;
  top_k: TopKPrediction[];
  recommendation?: {
    name_vi: string;
    name_en: string;
    description?: string;
    treatments: string[];
    severity?: string;
  };
  image_id?: string;
};

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";
