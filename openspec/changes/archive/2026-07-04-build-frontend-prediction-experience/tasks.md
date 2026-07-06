## 1. Phase 1 — Core Diagnosis (Shippable MVP)

- [x] 1.1 Audit `backend/app/models/schemas.py` to confirm all response fields before editing frontend types.
- [x] 1.2 Update `frontend/src/lib/api.ts`: add `prediction_id` and `latency_ms` to `PredictionResponse`, add all auth/knowledge/history types matching backend Pydantic schemas exactly.
- [x] 1.3 Create `frontend/src/lib/constants.ts` with `API_BASE_URL`, `MAX_FILE_SIZE_BYTES`, and `ALLOWED_IMAGE_TYPES`.
- [x] 1.4 Add API helper functions to `api.ts`: `registerUser`, `loginUser`, `getCurrentUser`, `fetchHistory`, `fetchKnowledgeList`, `fetchKnowledgeDetail`, with consistent error parsing that surfaces backend `detail` messages.
- [x] 1.5 Create `frontend/src/components/ImageUploader.tsx`: file select, drag-and-drop, camera capture via file input `capture` attribute, image preview with filename/size, reset action, client-side validation for jpeg/png/webp and 10 MB limit.
- [x] 1.6 Create `frontend/src/components/PredictionResult.tsx`: primary Vietnamese disease name (from `recommendation.name_vi`), model label, large confidence percentage with "Độ tin cậy" label, latency display, `recommendation.confidence_note` when available.
- [x] 1.7 Create `frontend/src/components/TopKList.tsx`: ranked top-k predictions with labels, confidence percentages, and proportional width confidence bars. Compute top-1/top-2 gap and show caution text when gap < 10%.
- [x] 1.8 Create `frontend/src/components/RecommendationCard.tsx`: render description, symptoms, causes, treatments, prevention, severity, advisory, and source links. Graceful fallback when recommendation is null.
- [x] 1.9 Create `frontend/src/components/ui/LoadingSpinner.tsx`, `ErrorMessage.tsx`, `EmptyState.tsx` for shared UI states.
- [x] 1.10 Create `frontend/src/hooks/usePrediction.ts`: manages file selection, upload mutation state, loading/error/result state. Preserves selected image on prediction failure.
- [x] 1.11 Refactor `frontend/src/app/page.tsx` to use the new components: ImageUploader + PredictionResult + TopKList + RecommendationCard. Keep as single page with diagnosis UI.
- [x] 1.12 Install `lucide-react` and use icons for upload, camera, reset, retry actions in ImageUploader.
- [x] 1.13 Verify `npm run build` passes with no type or compile errors.

## 2. Phase 2 — Features (Auth, Knowledge, History, Tabs)

- [x] 2.1 Create `frontend/src/hooks/useAuth.ts`: token persistence in localStorage (`plant_disease_token`), `login()`, `logout()`, `restore()` (calls `/auth/me` on mount, clears invalid token), `getAuthHeaders()`.
- [x] 2.2 Create `frontend/src/components/AuthForm.tsx`: login and register toggle form with username/email/password fields, clear success and error states.
- [x] 2.3 Create `frontend/src/components/AuthModal.tsx`: modal overlay wrapper for AuthForm, triggered from header user area.
- [x] 2.4 Update `frontend/src/components/ImageUploader.tsx` or `usePrediction.ts` to include `Authorization: Bearer <token>` when the user is authenticated.
- [x] 2.5 Create `frontend/src/components/KnowledgeList.tsx`: fetch and display supported diseases from `GET /api/v1/knowledge` with Vietnamese name, English name, crop, and severity. Includes loading/error states.
- [x] 2.6 Create `frontend/src/components/KnowledgeDetail.tsx`: fetch and display disease detail from `GET /api/v1/knowledge/{disease_label}` with symptoms, causes, treatments, prevention, sources.
- [x] 2.7 Create `frontend/src/components/HistoryList.tsx`: fetch paginated history from `GET /api/v1/history`, display predicted label, confidence, image URL, created time. Include loading/error/empty states. Prompt login for unauthenticated users.
- [x] 2.8 Create `frontend/src/components/TabNav.tsx`: three tabs (🔬 Chẩn đoán, 📚 Bệnh cây, 📋 Lịch sử) with active state highlighting.
- [x] 2.9 Update `frontend/src/app/page.tsx` to integrate TabNav with tab state, rendering DiagnosisPanel (existing result UI), KnowledgePanel (KnowledgeList + KnowledgeDetail), and HistoryPanel (HistoryList). Add header with user display name and login/logout action.
- [x] 2.10 Verify `npm run build` passes after Phase 2 changes.

## 3. Phase 3 — Polish (Responsive, Visual, Testing, Docs)

- [x] 3.1 Extend `frontend/tailwind.config.ts` with semantic colors: `surface`, `healthy`, `warning`, `danger`, `info` with 50/500/700 shades.
- [x] 3.2 Apply mobile-first responsive layout: single-column on mobile, grid layout on desktop (`lg:grid-cols-[...]`) for diagnosis/result panels.
- [x] 3.3 Add accessible labels, visible focus rings, semantic HTML sections (`<main>`, `<nav>`, `<section>`), and keyboard-reachable controls for core workflows.
- [x] 3.4 Review and refine color usage: replace one-note emerald with semantic colors (healthy for success, warning for low confidence, danger for errors, info for metadata).
- [x] 3.5 Install `vitest` and `@testing-library/jest-dom`. Create `frontend/vitest.config.ts`.
- [x] 3.6 Create `frontend/src/lib/__tests__/api.test.ts`: test `predictImage` sends FormData and handles success/error responses, test auth helpers include correct headers, test error parsing extracts `detail` messages.
- [x] 3.7 Add `"test": "vitest run"` script to `frontend/package.json` and verify tests pass.
- [x] 3.8 Update `frontend/.env.example` with documented `NEXT_PUBLIC_API_BASE_URL`.
- [x] 3.9 Update `frontend/README.md`: implemented features, setup steps, `npm run dev`/`build`/`test` commands, API base URL configuration, known limitation that segmentation overlays are not available until backend returns geometry.
- [x] 3.10 Final `npm run build` and `npm run lint` verification.
