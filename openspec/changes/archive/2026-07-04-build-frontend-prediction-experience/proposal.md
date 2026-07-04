## Why

The frontend is a minimal single-page upload flow (~200 LOC total) while the backend already exposes prediction, knowledge, auth, and history endpoints. The project requires a mobile-first diagnostic tool demonstrating image upload, confidence/top-k inspection, Vietnamese expert recommendations, authenticated history, and disease knowledge browsing before the final demo and report phase.

This change is needed now because the backend API contract is stable and the frontend must catch up to deliver a complete user-facing experience.

## What Changes

- Componentize the monolithic `page.tsx` into focused UI modules: image upload, prediction result, top-k confidence list, recommendation card, knowledge browser, auth form, history list, and shared UI states.
- Sync frontend TypeScript types with backend Pydantic schemas, adding missing `prediction_id`, `latency_ms`, and all auth/knowledge/history types.
- Add client-side validation for supported image formats (jpeg/png/webp) and the 10 MB upload limit before calling `/api/v1/predict`.
- Build a single-page application with client-side tab navigation for three sections: diagnosis, disease knowledge browsing, and authenticated prediction history.
- Add auth flows (register, login, `/auth/me` restore, logout, token persistence) using the existing backend JWT endpoints.
- Add a knowledge browser backed by `/api/v1/knowledge` and `/api/v1/knowledge/{disease_label}`.
- Make confidence and top-k first-class trust signals: large confidence display, ranked alternatives with visual bars, and caution copy when top predictions are close.
- Improve UI/UX with mobile-first responsive layout, accessible controls, loading/error/empty states, and a balanced color system beyond one-note green.
- Add `lucide-react` for icons and `vitest` for API client unit tests.
- Keep the result UI compatible with the current classification-style backend response, reserving structure for future segmentation overlays.

## Capabilities

### New Capabilities

- `frontend-prediction-experience`: Covers the user-facing Next.js frontend for image diagnosis, confidence/top-k inspection, Vietnamese disease recommendations, authenticated history, disease knowledge browsing, responsive UI, and verification requirements.

### Modified Capabilities

- None.

## Impact

- Affected frontend code: `frontend/src/app/page.tsx`, `frontend/src/lib/api.ts`, new components/hooks/types under `frontend/src/`.
- Affected docs: `frontend/README.md` for setup, features, and test commands.
- Affected API contracts: consumes existing FastAPI endpoints under `/api/v1` without changing backend behavior.
- Affected configuration: `frontend/.env.example` for `NEXT_PUBLIC_API_BASE_URL`.
- Affected verification: `npm run build`, `npm run lint`, Vitest API client tests.
- New dependencies: `lucide-react` (icons), `vitest` + `@vitest/jsdom` (testing). No SWR, no shadcn/ui, no Playwright.
- Implementation is structured in 3 phases: Core diagnosis (shippable MVP), Features (auth/knowledge/history), and Polish (responsive/testing/docs).
