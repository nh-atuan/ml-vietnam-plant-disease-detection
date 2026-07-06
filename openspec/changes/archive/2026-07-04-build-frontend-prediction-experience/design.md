## Context

The project is a Vietnamese plant disease detection system for rice and coffee leaves. The frontend is responsible for Phase 5.4: a mobile-first Next.js application that connects to the FastAPI backend for image diagnosis, confidence inspection, expert recommendations, authenticated history, and disease knowledge browsing.

Current frontend state:

- `frontend/` contains a Next.js 15, React 19, Tailwind 3 app.
- `frontend/src/app/page.tsx` is a single client page (~137 LOC) with upload, submit, result, top-k, and recommendation rendering.
- `frontend/src/lib/api.ts` calls `POST /api/v1/predict`, but `PredictionResponse` is missing `prediction_id` and `latency_ms`.
- No auth, no knowledge browsing, no history, no tests, no routing beyond the single page.
- The frontend README lists componentization, camera/drag-drop, history, responsive UX, and API integration as TODOs.

Current backend API state:

- Backend base URL via `NEXT_PUBLIC_API_BASE_URL`, defaulting to `http://localhost:8000/api/v1`.
- Endpoints: `/api/v1/predict`, `/api/v1/knowledge`, `/api/v1/knowledge/{disease_label}`, `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/auth/me`, `/api/v1/history`.
- `/api/v1/predict` accepts jpeg/png/webp up to 10 MB, returns `prediction`, `confidence`, `top_k`, optional `recommendation`, `image_id`, `image_url`, `prediction_id`, and `latency_ms`.
- `/api/v1/auth/login` returns `{ access_token, token_type }`.
- `/api/v1/history` returns `{ items, total, page, page_size }` with pagination.
- The backend does not return segmentation masks or boxes.

## Goals / Non-Goals

**Goals:**

- Deliver a frontend that accurately consumes the existing FastAPI API contract across all endpoints.
- Use a single-page app with client-side tabs (Diagnosis, Knowledge, History) — no file-based routing beyond the root page.
- Make confidence and top-k first-class trust signals, not secondary debug information.
- Keep anonymous prediction usable even when auth services are unavailable.
- Support 3-phase implementation: Core (shippable MVP) → Features (auth/knowledge/history) → Polish (responsive/testing/docs).
- Add only `lucide-react` and `vitest` as new dependencies.

**Non-Goals:**

- Do not change backend endpoints, database schema, or inference implementation.
- Do not add segmentation overlays until the backend returns mask/box geometry.
- Do not replace backend JWT auth with Clerk, Auth0, or any third-party auth.
- Do not add SWR, shadcn/ui, Playwright, React Testing Library, or other heavy dependencies.
- Do not create multi-page file-based routes — keep everything in the root page with client tabs.
- Do not own Kubernetes, Helm, or CI/CD deployment configuration.

## Decisions

### Decision 1: Single-page with client-side tabs, not file-based routing

The app will stay as a single `page.tsx` shell with three client-side tab panels: DiagnosisPanel, KnowledgePanel, and HistoryPanel. Auth uses a modal overlay, not a separate route.

Rationale:

- The app is a diagnostic tool, not a content website — users should never lose context of where they are.
- Single-page avoids RSC/SSR complexity for data that requires client auth tokens.
- Tab state can be managed with a simple `useState` — no router library needed.
- Auth modal keeps the main workflow visible and avoids a login page dead-end.

Alternatives considered:

- File-based routes (`/knowledge`, `/history`): adds complexity with `useRouter`, layout nesting, and shared state propagation without clear UX benefit.
- Full SPA router (react-router): unnecessary dependency for 3 tabs.

### Decision 2: Componentize into focused modules

Split the monolithic page into ~13 component files + 2 hooks + 2 lib files:

```
frontend/src/
├── components/
│   ├── ImageUploader.tsx       ← Drag-drop, file select, camera, preview
│   ├── PredictionResult.tsx    ← Primary label + confidence percentage
│   ├── TopKList.tsx            ← Ranked alternatives with confidence bars
│   ├── RecommendationCard.tsx  ← Vietnamese expert knowledge
│   ├── KnowledgeList.tsx       ← Supported diseases grid
│   ├── KnowledgeDetail.tsx     ← Single disease detail view
│   ├── AuthForm.tsx            ← Login + Register toggle form
│   ├── AuthModal.tsx           ← Modal wrapper for auth form
│   ├── HistoryList.tsx         ← Paginated history items
│   ├── TabNav.tsx              ← Tab navigation shell
│   └── ui/
│       ├── LoadingSpinner.tsx
│       ├── ErrorMessage.tsx
│       └── EmptyState.tsx
├── hooks/
│   ├── useAuth.ts              ← Token management + user state
│   └── usePrediction.ts       ← Upload mutation state
└── lib/
    ├── api.ts                  ← Typed API client (all endpoints)
    └── constants.ts            ← API URL, file limits, etc.
```

Rationale:

- Component boundaries map directly to backend API responses and UI sections.
- Each component can be built and tested independently.
- ~17 new files is manageable for a single PR.

### Decision 3: Typed API client as single source of truth

All API calls go through `frontend/src/lib/api.ts` with TypeScript types matching backend Pydantic schemas exactly.

Types to add:

```typescript
// Missing from current api.ts:
prediction_id?: string;
latency_ms?: number;

// Entirely new types needed:
UserCreate, UserResponse, LoginRequest, TokenResponse,
HistoryItem, HistoryResponse, KnowledgeListResponse
```

API functions to add:

```typescript
registerUser(data: UserCreate): Promise<UserResponse>
loginUser(data: LoginRequest): Promise<TokenResponse>
getCurrentUser(token: string): Promise<UserResponse>
fetchHistory(token: string, page?: number): Promise<HistoryResponse>
fetchKnowledgeList(): Promise<KnowledgeListResponse>
fetchKnowledgeDetail(label: string): Promise<DiseaseRecommendation>
```

Rationale:

- Single file to update when backend schemas change.
- Centralizes auth header injection and error parsing.

### Decision 4: Confidence and top-k as first-class trust signals

The result screen will show:

- Primary confidence as a large percentage with "Độ tin cậy" label.
- `recommendation.confidence_note` when available from the backend.
- Top-k as a ranked list with proportional confidence bars.
- Client-side top-1/top-2 gap check: if gap < 10%, show caution text advising the user to compare symptoms or retake the image.
- Advisory copy that model output is decision support, not a definitive diagnosis.

Rationale:

- Agricultural users need to judge whether to trust a prediction or retake the image.
- Visual confidence bars make top-k comparison intuitive without reading numbers.

### Decision 5: Minimal dependency strategy

| Package | Decision | Rationale |
| --- | --- | --- |
| `lucide-react` | ✅ Add | Lightweight tree-shakeable icons for upload/camera/reset/retry/login actions |
| `vitest` | ✅ Add | Fast test runner for API client unit tests |
| `@testing-library/react` | ❌ Skip | Component tests are optional given project timeline |
| `SWR` | ❌ Skip | Custom `useAuth` hook with `useEffect` + fetch is sufficient for 3 authenticated endpoints |
| `shadcn/ui` | ❌ Skip | Tailwind utility classes are already available and sufficient |
| `Playwright` | ❌ Skip | Full browser E2E requires running backend stack; manual testing against local backend is more practical |

### Decision 6: Simple 5-color visual system

Extend existing Tailwind config with semantic colors:

```typescript
// tailwind.config.ts extend.colors
surface: { DEFAULT: '#f7f9f6', raised: '#ffffff' },
healthy: { 50: '#f0fdf4', 500: '#22c55e', 700: '#15803d' },
warning: { 50: '#fffbeb', 500: '#f59e0b', 700: '#b45309' },
danger:  { 50: '#fef2f2', 500: '#ef4444', 700: '#b91c1c' },
info:    { 50: '#eff6ff', 500: '#3b82f6', 700: '#1d4ed8' },
```

Usage mapping:

- `healthy` → high confidence, healthy leaf result, success states
- `warning` → low confidence, close top-k gap, severity warnings
- `danger` → disease severity, error states, validation failures
- `info` → links, latency display, metadata, neutral actions
- Stone/neutral → text, borders, surfaces (already used)

Rationale: Avoids the one-note emerald-green palette of the current page while staying cohesive.

### Decision 7: Auth token in localStorage

Store JWT in `localStorage` under key `plant_disease_token`. The `useAuth` hook handles:

- `login()` → stores token, fetches `/auth/me`, sets user state
- `logout()` → clears token and user state
- `restore()` → on mount, checks localStorage for token, calls `/auth/me`, clears if invalid
- `getAuthHeaders()` → returns `{ Authorization: Bearer <token> }` or empty object

Rationale:

- Simple, no server-side session needed.
- Acceptable for a class project demo; not recommended for production.
- Token only sent as `Authorization: Bearer`, never exposed elsewhere.

### Decision 8: 3-phase execution strategy

**Phase 1 — Core Diagnosis (shippable MVP):**
Refactor api.ts types, componentize page.tsx, image validation, drag-drop upload, confidence/top-k trust UI, recommendation display, loading/error states. `npm run build` must pass.

**Phase 2 — Features:**
Auth flow (register/login/logout/me), token persistence, history listing with pagination, knowledge browser (list + detail), tab navigation shell.

**Phase 3 — Polish:**
Mobile-first responsive pass, visual system refinement (colors/spacing/icons), Vitest API client tests, README update.

Rationale:

- Phase 1 produces a demo-ready product even if time runs out.
- Phase 2 adds completeness features that enhance the demo.
- Phase 3 adds quality but is expendable under deadline pressure.

## Risks / Trade-offs

- [Backend services unavailable locally] → Keep error states explicit. Show backend `detail` messages. Allow anonymous prediction to work without auth services.
- [Single PR scope is large] → 3-phase execution means Phase 1 is shippable on its own. Each phase builds on the previous without breaking it.
- [localStorage token security] → Acceptable for class project demo. Document the limitation.
- [No E2E test coverage] → Manual testing against local backend. Vitest covers API client edge cases.
- [Tab navigation loses URL state] → Users can't bookmark tabs. Acceptable for a diagnostic tool that always starts at the diagnosis tab.
- [No SWR means manual loading state management] → Custom hooks handle this for 3-4 authenticated endpoints. Would not scale to many more endpoints.

## Open Questions

- None. All design decisions are resolved. Implementation-time discoveries should be captured as task notes.
