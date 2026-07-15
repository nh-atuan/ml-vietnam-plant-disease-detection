# UI Improvement Audit and Implementation Plan

**Audit date:** 2026-07-15

**Branch audited:** `refactor/improve-ui` at `08d3291`

**Implementation status:** Audit and planning only; no production UI code was changed.

## 1. Executive summary

The current frontend is operational and its core backend integrations work, but it is not ready for a UI/UX-only production refresh without first repairing several interaction, accessibility, content, and environment-boundary defects. The local stack returned HTTP 200 for both the frontend and backend health endpoint. Registration, automatic login, logout on desktop, knowledge browsing, authenticated history, light/dark theme switching, and the prediction API were exercised successfully against local services. Frontend unit tests, TypeScript checking, lint, and production build also completed successfully.

No P0 issue was confirmed. Five P1 issues were confirmed:

1. Authenticated users have no account controls or logout action at mobile and tablet widths.
2. The authentication modal is not an accessible dialog and cannot be dismissed with Escape.
3. Authentication form labels and errors are not programmatically associated with their inputs.
4. Knowledge cards and history rows are mouse-only, blocking keyboard users from core content.
5. The checked-in frontend API fallback/template targets production, which can make a host-run local frontend write test data to production if `.env.local` is missing or copied without editing.

The observed “broken” Login and Registration presentation is caused by more than visual taste. The close button uses Tailwind utilities that are not generated, so it is absent or overlaps the modal title; the modal has no focus management; fields are exposed to assistive technology by placeholder instead of label; raw English API errors are displayed; and mobile/tablet users cannot access account or logout controls after authenticating.

The recommended approach is an incremental academic-demo repair, not a rewrite. Keep modal auth, JWT `localStorage`, the current single-page tabs, and existing backend contracts. First wire “Chẩn đoán mới” to the existing reset handler, replace the broken auth overlay and cramped logout action with targeted Radix Dialog/DropdownMenu primitives, and finish the existing history pagination. Then remove internal content and technical result metadata, apply focused responsive/accessibility polish, and add regression coverage. Password reset, HttpOnly cookies, deep-link routing, and a broad design-system migration are explicitly excluded.

### Severity summary

| Severity | Count | Summary |
| --- | ---: | --- |
| P0 | 0 | No confirmed sensitive-data leak, destructive behavior, or total application failure. |
| P1 | 5 | Mobile/tablet logout, modal accessibility, auth field semantics, keyboard-blocked core content, local-to-production API risk. |
| P2 | 20 | Stale auth state, reset and pagination behavior, raw/internal content, misleading trust language, missing CSS output, responsive/history gaps, missing UI tests, and maintainability problems. |
| P3 | 5 | Visual density, token naming/drift, semantic polish, route deep-linking, and tooling cleanup. |

## 2. Current frontend architecture summary

| Concern | Current implementation |
| --- | --- |
| Framework | Next.js 15.5 App Router, React 19, TypeScript strict mode. |
| Routing | One application route, `/`, implemented by `frontend/src/app/page.tsx`. Diagnosis, knowledge, and history are local-state tabs rather than URL routes. The default Next.js `/_not-found` page handles unknown URLs. |
| Rendering | The complete application page is a client component. The shell, tabs, dialogs, and feature state are composed in `page.tsx`. |
| Authentication | Login and registration share an `AuthForm` inside an overlay `AuthModal`. Registration automatically logs the new user in. JWT is stored in `localStorage` by `useAuth`. There is no forgot-password or password-reset API/UI. |
| State management | React `useState`, `useEffect`, and two custom hooks (`useAuth`, `usePrediction`). There is no global state library, query cache, router-backed state, or form library. |
| API integration | A hand-written `fetch` client in `frontend/src/lib/api.ts`, using `NEXT_PUBLIC_API_BASE_URL`. It directly exposes backend `detail` strings as `Error.message`. |
| Styling | Tailwind CSS 3.4, CSS custom-property color tokens in `globals.css`, and component-local utility strings. Light/dark mode is class-based and persisted in `localStorage`. |
| Component library | No external UI component library is currently installed. There are local feature components and three small state components (`LoadingSpinner`, `ErrorMessage`, `EmptyState`), but no shared Button, IconButton, Dialog, FormField, Tabs, or Card primitives. This plan adds Radix Primitives incrementally for Dialog and DropdownMenu behavior only. |
| Icons | `lucide-react`. Some icon-only controls rely on `title`; several have no accessible name. |
| Motion | `framer-motion` for page/section entrances plus Tailwind transition classes. No reduced-motion policy is implemented. Several Tailwind animation class names are not compiled. |
| Typography | Inter, Be Vietnam Pro, and Playfair Display through `next/font`. Be Vietnam Pro is the display face, Inter is the body face, and Playfair is used for the product mark. |
| Testing | One Vitest file with 9 API-client tests. React Testing Library is installed but no component test exists. No Playwright config, E2E test, Storybook, or visual regression suite exists. |
| Backend contract | `/api/v1/predict` returns classification-style `prediction`, `confidence`, `top_k`, optional recommendation, image identifiers/URL, prediction ID, and latency. It does not return segmentation masks or boxes. Auth provides register/login/me; history is JWT-protected. |

The architecture is small enough to improve in place. The main maintainability problem is not framework choice; it is the lack of semantic UI primitives and status-aware API/auth boundaries.

## 3. Audit scope and inspection methodology

### Repository and documentation inspection

- Checked the branch, working tree, commit, Docker Compose services, frontend package scripts, Next/Tailwind/TypeScript/Vitest configuration, all frontend source files, relevant backend auth/predict contracts, and deployment configuration.
- Read the root and frontend README files; the docs index; development guide; web/final plans; API documentation; integration/load testing guide; deployment runbooks; project requirements; and UI-relevant sections of the proposal and reports.
- Searched source and rendered content for version strings, internal names, environment URLs, debug/development language, technical IDs, placeholders, tokens, and raw errors.
- Searched for design-system documentation, Figma links, Storybook, mockups, UI screenshots, brand guidelines, and browser tests. None were found for the product UI.
- `AGENTS.md` does not exist in the repository or its checked parent directory, so there were no repository-local agent instructions to apply.

### Runtime inspection

- Reused the running local Docker Compose stack at `http://localhost:3000` and `http://localhost:8000`.
- Used the in-app Browser and its Playwright DOM APIs at representative widths of 375, 768, and 1440 CSS pixels.
- Inspected diagnosis, Login, Registration, authenticated shell, unauthenticated and authenticated history, history detail, knowledge list/detail, theme switching, logout, validation errors, backend login errors, and the default not-found route.
- Created one local-only audit account and one local prediction/history record. No production data was used or modified.
- Checked browser console warnings/errors. None were captured during the inspected flows.
- Measured document overflow, element bounds, control target sizes, focus state, modal semantics, accessible names, and layout offsets from the rendered DOM.
- Used source inspection for states that cannot be forced safely through the current UI, including expired JWT handling and backend inference/storage exception rendering.

### Automated checks

```bash
cd frontend
npm test
npx tsc --noEmit
npm run lint
npm run build
```

Results: 9/9 tests passed; TypeScript passed; lint passed with a deprecated-command notice and one `@next/next/no-img-element` warning; the production build passed.

### Frontend command inventory

| Purpose | Command | Current status |
| --- | --- | --- |
| Reproducible dependency install | `cd frontend && npm ci` | Supported by the committed lockfile. Documentation currently says `npm install`. |
| Start full local stack | `docker compose up --build -d` | Confirmed; frontend is `http://localhost:3000`, backend is `http://localhost:8000`. |
| Start host-run frontend | `cd frontend && npm run dev` | Supported; requires a local-targeted `.env.local`. |
| Start built frontend | `cd frontend && npm run start` | Supported after `npm run build`. |
| Unit tests | `cd frontend && npm test` | Confirmed passing, 9/9 API-client tests. |
| Lint | `cd frontend && npm run lint` | Confirmed passing with one image warning; command is deprecated by Next.js. |
| Type check | `cd frontend && npx tsc --noEmit` | Confirmed passing; no package script exists yet. |
| Production build | `cd frontend && npm run build` | Confirmed passing with the same image warning. |

No tables, dropdown menus, breadcrumbs, conventional footer, toast/notification system, or standalone auth routes exist in the current UI. Loading states were inspected in source and during transient browser transitions; the local API was fast enough that not every loading frame could be retained as visual evidence.

## 4. Known constraints and assumptions

- The task is documentation-only. Production UI source, backend APIs, database schemas, and deployment code were not modified.
- The browser loaded the local Docker-built frontend and local API. The current untracked `frontend/.env.local` was classified as local-targeted without exposing its value.
- The checked-in `.env.example`, API fallback, and Dockerfile default still target the public deployment. That is an environment-safety defect even though this audit session used local services.
- No external brand guideline, Figma source, or formal design system is present. The implementation must use the product/content decisions below as its baseline and must not invent additional brand claims.
- There is no forgot-password/reset contract. Password recovery is deferred to a separately scoped backend-enabled feature and must not appear as a dead link in this UI release.
- The model/API currently provides classification-style output only. A UI improvement must not invent segmentation overlays, boxes, masks, or calibrated probability claims.
- The recommendation knowledge base supplies an advisory for some records, but the UI must not assume every recommendation has one.
- Only the two reliable mobile screenshots were retained. Desktop/tablet evidence is based on DOM snapshots and measured bounds because the in-app Browser screenshot capture produced inconsistent scaling for inactive or large viewports.
- A full screen-reader pass, real iOS safe-area test, real Android camera permission test, 200% browser zoom pass, and cross-browser matrix were not completed in this audit.

### 4.1 Product and implementation decisions

The following decisions resolve the UI questions for planning purposes. They apply to this improvement effort unless the project owner explicitly overrides them before implementation.

| ID | Decision | Rationale and implementation boundary |
| --- | --- | --- |
| DEC-01 | Use **PlantDisease AI** as the public product name, with the Vietnamese descriptor **“Nhận diện bệnh cây từ ảnh lá”** where supporting context is needed. Retain the current neutral plant/leaf mark until an approved logo asset exists. | `PlantDisease AI` is already the only product name used consistently in the rendered shell. Do not expose `Claude UI`, `Studio`, `Dashboard`, account tiers, model/framework names, or a version string in normal user-facing UI. Build/release versions may remain in deployment metadata and support logs. |
| DEC-02 | Call the model output **“Kết quả dự đoán”** and the leading class **“Dự đoán hàng đầu”**. Display **“Điểm tin cậy của mô hình”**, not probability, accuracy, certainty, or “chẩn đoán chính xác”. | The repository proposes future calibration work but provides no completed ECE/Brier/reliability evidence. Present top-k as **“Các kết quả khác mô hình đã cân nhắc”**. Surface backend `confidence_note` when present; do not invent a frontend low-confidence threshold without an ML-owner decision. |
| DEC-03 | Show a persistent agronomic disclaimer with every prediction and treatment recommendation. | Approved baseline wording for the plan: **“Kết quả do mô hình AI tạo ra chỉ nhằm mục đích tham khảo, không thay thế đánh giá trực tiếp của chuyên gia bảo vệ thực vật. Hãy đối chiếu triệu chứng thực tế và tham khảo cán bộ kỹ thuật trước khi sử dụng thuốc hoặc áp dụng biện pháp xử lý.”** A record-specific backend advisory may supplement but never replace this baseline. |
| DEC-04 | Keep Login and Registration in the existing modal flow for this academic demo. Replace the hand-built overlay with Radix Dialog while retaining the shared `AuthForm`. | Dedicated auth routes are not required for the current demo. Radix Dialog supplies the difficult modal behavior already missing from the implementation: focus management, Escape dismissal, accessible title/description, and focus restoration. The close button must occupy a reserved header slot and remain 44x44 px instead of being absolutely positioned over the title. Registration keeps automatic login because no verification step exists. |
| DEC-05 | Forgot/reset password is **out of scope** for this UI release. | The backend has no email, reset-token, or password-reset contract. Do not render a non-functional “Quên mật khẩu?” link and do not create a recovery task in this plan. Reconsider only if the course-project scope changes. |
| DEC-06 | Keep JWT in `localStorage`; no HttpOnly-cookie migration task is included in this plan. | `localStorage` is accepted for the academic demo. The UI must still clear the token on logout or 401, avoid stale authenticated state, and never render untrusted HTML. Broader session-security architecture is outside the UI/UX scope. |
| DEC-07 | Keep the current single-page, local-state navigation. Deep links and browser-back integration are out of scope. | Knowledge and history remain tabs/details within `/`. This avoids an App Router and backend-contract expansion that does not materially improve the course demo. Pagination state may reset when leaving history or refreshing the page. |
| DEC-08 | Remove raw model label and prediction UUID from normal user-facing views; retain latency as **“Thời gian phản hồi mô hình”**. | Latency is an intentional academic-demo performance metric for lecturer evaluation. Show it beside confidence in milliseconds when supplied by the API, without displacing disease name, top-k, or recommendations. |
| DEC-09 | Use WCAG 2.2 AA as implementation guidance for critical interactions, not as a formal conformance certification. Primary browser acceptance is current desktop Chrome/Chromium plus responsive emulation at 375, 768, and 1440 px. | Keyboard operation, labels, visible focus, dialog behavior, meaningful contrast, and status announcements remain required because they directly improve usability. Firefox/Safari and real Android/iOS checks are best-effort smoke checks when devices are available, not release blockers for the course demo. |
| DEC-10 | Adopt Radix Primitives incrementally for complex interaction behavior; keep Tailwind, Lucide, and existing feature components. | Use the tree-shakeable `radix-ui` package only for primitives actually needed in this scope, initially `Dialog` for auth and `DropdownMenu` for account/logout. Do not add Radix Themes, MUI, Ant Design, or a generated component collection. Keep small project-specific wrappers (`Button`, `IconButton`, `FormField`, `Pagination`) only where they eliminate repeated Tailwind/ARIA code. Radix documents incremental adoption, unstyled integration, focus management, and keyboard behavior: https://www.radix-ui.com/primitives/docs/overview/introduction. |

### 4.2 Academic-demo delivery priorities

The implementation order is intentionally narrower than a production SaaS redesign:

1. Repair the broken “Chẩn đoán mới” action by wiring the existing `handleReset` into a single `startNewDiagnosis` handler.
2. Repair the Login/Registration close control and modal behavior with Radix Dialog.
3. Replace the cramped standalone logout icon with an account DropdownMenu that cannot overlap the username/content and is reachable on mobile/tablet.
4. Finish and verify history pagination. The source already has conditional previous/next logic with `PAGE_SIZE = 5`; the work is to make it reusable, labelled, visible with more than five records, and robust across loading/error/page-boundary states.
5. Remove internal copy and technical result metadata, then perform targeted visual, responsive, and accessibility cleanup.
6. Add focused component/browser regression tests for these demo-critical flows. Do not expand into password recovery, cookie migration, deep-link routing, a new backend history-detail API, or a wholesale component rewrite.

## 5. Route and feature inventory

| Route or state | Availability | Primary components | Notes |
| --- | --- | --- | --- |
| `/` diagnosis, empty | Public | `page.tsx`, `ImageUploader`, `Sidebar`, `Header` | Default state. File input and camera input are hidden behind controls. |
| `/` diagnosis, loading | Public/authenticated | `LoadingSpinner`, result grid shell | Local component state; no URL/state persistence. |
| `/` diagnosis, success | Public/authenticated | `PredictionResult`, `TopKList`, `RecommendationCard` | Authenticated predictions are saved to history. No masks/boxes exist in the API. |
| `/` diagnosis, error | Public/authenticated | `ImageUploader` inline error | Directly renders API error strings. |
| `/` knowledge list | Public | `KnowledgeList`, `BentoGrid` | Cards are click-only `div` elements. |
| `/` knowledge detail | Public | `KnowledgeDetail`, `RecommendationCard` | Selected disease is local state; no deep link. |
| `/` history, unauthenticated | Public | `HistoryList` login prompt | Entry point to auth on mobile/tablet. |
| `/` history, authenticated empty | Authenticated | `HistoryList`, `EmptyState` | Explains next step but has no CTA. |
| `/` history, authenticated list/detail | Authenticated | `HistoryList`, `RecommendationCard` | Row is click-only; confidence disappears below `sm`. Conditional previous/next pagination exists only when `total > 5` and needs usability/testing work. |
| Login overlay | Public | `AuthModal`, `AuthForm` | No standalone `/login` route. |
| Registration overlay | Public | `AuthModal`, `AuthForm` | Auto-login after register. No password confirmation or account-policy content. |
| Forgot/reset password | Not implemented | None | No frontend route and no backend endpoint. |
| Account/logout | Desktop only | `Sidebar` | Missing below `lg` (mobile and tablet). |
| Unknown route | Public | Next.js default `/_not-found` | English-only default page with no app navigation. |

## 6. Detailed findings grouped by category

Each confirmed finding includes a concrete route/state, source location, reproduction, expected and actual behavior, impact, cause, evidence, remediation direction, and dependency/blocker status.

### A. Functional correctness and authentication

| ID | Severity | Route / state and source | Reproduction and evidence | Expected vs actual / impact | Technical cause and recommended direction | Blocks |
| --- | --- | --- | --- | --- | --- | --- |
| UI-AUTH-001 | P1 | `/`, authenticated, 375 and 768 px. `frontend/src/components/Sidebar.tsx:49`, `:159` | Register/login locally, resize to 375 or 768 px, inspect navigation. Browser measured `visibleLogoutButtons: 0`; desktop logout works at 1440 px. The project owner also reports that the current desktop logout control can overlap adjacent account content. | Expected: account identity and logout remain reachable at every supported width without colliding with the username or shell. Actual: the entire auth section is inside the desktop-only sidebar; mobile/tablet show only three tabs, while desktop uses a cramped standalone icon action. | Use a Radix DropdownMenu account trigger with collision handling and a labelled logout item. Render the same account action in mobile/tablet navigation and desktop sidebar; constrain/truncate the username and test long names. | Phase 1/2. |
| UI-AUTH-002 | P1 | Login/Registration overlay, all widths. `AuthModal.tsx:14` | Open auth. Browser found zero `dialog`/`role=dialog`, zero `aria-modal`, focus stayed on the background opener, and Escape left the modal open. Source contains no focus trap or focus-restoration logic. | Expected: a modal has a name, traps focus, moves initial focus inside, closes with Escape, restores focus, and prevents background interaction. Actual: it is only positioned `div` elements with body scroll locking. Keyboard and screen-reader users can become disoriented or interact behind it. | Replace the hand-built overlay with Radix Dialog. Put `Dialog.Close` in a reserved modal-header slot, use `Dialog.Title`/`Description`, preserve backdrop dismissal, and visually verify that the 44x44 px close target never overlaps Login or Registration content. | Phase 1; prerequisite for auth polish. |
| UI-AUTH-003 | P1 | Login/Registration form. `AuthForm.tsx:86` | Browser reported `associatedLabels: 0` for username, email, and password. Textboxes were exposed by placeholder. Client and backend errors had no `role=alert` and inputs had no `aria-describedby`. | Expected: visible labels are programmatically bound; invalid fields expose `aria-invalid` and linked error/help text. Actual: labels lack `htmlFor` and inputs lack IDs; a screen reader cannot reliably connect fields to labels/errors. Critical auth validation is visually present only. | Introduce `FormField` markup with stable IDs, `htmlFor`, autocomplete values, descriptions, per-field errors, an error summary/live region, and focus on the first invalid field. Localize server errors. | Phase 2. |
| UI-AUTH-004 | P2 | Auth/history after expired or invalid JWT. `useAuth.ts:13`, `HistoryList.tsx:26`, `api.ts:88` | Source path: session is validated only on mount. Later history 401 is converted to a generic `Error`; user/token remain set and history renders the error. Backend returns English credential details. | Expected: a 401 atomically clears stale auth state, explains session expiration, and offers login while preserving safe context. Actual: stale identity can remain in the shell until logout/reload; on mobile, logout is unavailable. | Return a typed API error containing status/code. Centralize unauthorized handling in `useAuth`/API client, clear session, show localized “session expired”, and reopen or link to login. Requires no schema change if status is preserved; backend error codes would improve localization. | Phase 1/2; related to UI-ARCH-003. |
| UI-FUNC-001 | P2 | `/`, diagnosis after a successful/selected prediction. `page.tsx:22`, `usePrediction.ts:37`, `Sidebar.tsx:119` | `usePrediction` returns `handleReset`, but `page.tsx` does not consume it. “Chẩn đoán mới” only calls `onTabChange("diagnosis")`. | Expected: “New diagnosis” clears the prior file, error, loading, and result state, or asks before discarding active work. Actual: when already on diagnosis or returning to it, stale state remains. The action label does not match behavior. | Define one `startNewDiagnosis` action that resets prediction state and selected disease as appropriate, then navigates. Add a component/E2E regression test. | Phase 1. |
| UI-FUNC-002 | P2 | Unknown URL. No `frontend/src/app/not-found.tsx`. | Browser opened `/ui-audit-nonexistent` and rendered “404 — This page could not be found.” under `lang="vi"`, with no app navigation. | Expected: a Vietnamese, branded, actionable not-found state. Actual: the default English Next page is inconsistent and creates a dead end. | Add `not-found.tsx` using the normal shell or a lightweight public header with links to diagnosis and knowledge. | Phase 1 or 4. |
| UI-FUNC-003 | P2 | `/`, authenticated history. `HistoryList.tsx:17`, `:30`, `:230` | Source contains API-backed pagination with `PAGE_SIZE = 5`, but it renders only when `totalPages > 1`, exposes only two small icon arrows, has no accessible names, and was not exercised in the audit because the local account had fewer than six records. The project owner reports pagination as effectively absent. | Expected: once history exceeds one page, users can discover the current page, move backward/forward, understand disabled boundaries, and recover from page-loading errors. Actual: the conditional compact control is easy to miss and lacks an accessible contract; multi-page behavior has no regression coverage. | Extract a small `Pagination` component using the existing Button/IconButton styling, labelled previous/next controls, current-page text, 44 px targets, loading protection, and a test fixture with at least 11 items. Keep the existing backend `page`/`page_size` contract; no backend change is required. | Phase 1. |

### B. Information exposure, content, and trust

| ID | Severity | Route / state and source | Reproduction and evidence | Expected vs actual / impact | Technical cause and recommended direction | Blocks |
| --- | --- | --- | --- | --- | --- | --- |
| UI-CONTENT-001 | P2 | Desktop sidebar/auth/header. `Sidebar.tsx:180`, `:214`; `AuthModal.tsx:49`; `page.tsx:66` | Rendered UI visibly contains `v1.2.0 · Claude UI`, `Tài khoản Studio`, `Thành viên Free`, and `Chẩn đoán Dashboard`. Source search found the same hard-coded strings. | Expected: product-facing Vietnamese language aligned with approved branding and actual entitlements. Actual: implementation/tool names, an unsupported “Free” tier, and mixed internal English leak into the product. This weakens trust and may misrepresent account status. | Remove version/tool attribution unless legal/product explicitly requires it. Replace Studio/Dashboard/Free with approved product language. Keep release versions in diagnostics/build metadata, not primary UI. | Phase 0 decision for product name; Phase 1 cleanup. |
| UI-CONTENT-002 | P2 | Diagnosis success. `PredictionResult.tsx:38`, `:78`, `:93` | Source renders raw label in `<code>`, inference latency in milliseconds, and prediction UUID to every user. | Expected: primary results prioritize disease name, confidence context, next steps, and sources; technical metadata is absent or behind an intentional diagnostics affordance. Actual: internal label/latency/ID compete with the decision content and expose implementation details. | Hide ID and latency from normal users. Show raw labels only if a documented support/export use case exists; otherwise keep them in logs/API. | Phase 1. |
| UI-TRUST-001 | P2 | Diagnosis and knowledge detail. `PredictionResult.tsx:27`; `RecommendationCard.tsx:91` | Rendered headings say “Chẩn đoán chính xác nhất” and “Tư vấn kỹ thuật chuyên nghiệp”. The disclaimer is conditional on `recommendation.advisory`; no persistent AI/field-verification statement exists. | Expected: calibrated language such as “Kết quả dự đoán hàng đầu” and consistent guidance to verify field symptoms/consult local plant-protection expertise before treatment. Actual: copy overstates certainty and expertise, especially when confidence is low or the advisory field is absent. | Establish a trust-content rule: never call model output exact; always show confidence context and a baseline advisory; preserve stronger record-specific advisories. Confirm wording with the ML/agronomy owner. | Phase 0 content decision; Phase 1 cleanup. |
| UI-ERROR-001 | P2 | Login, predict, history, knowledge errors. `api.ts:88`; `backend/app/routers/predict.py:80`; `backend/app/routers/auth.py:27` | Browser confirmed raw English `Incorrect username or password`. Source shows frontend directly renders backend `detail`, including `Inference failed: {exc}` and `Storage or database unavailable: {exc}`. | Expected: localized, actionable, non-sensitive messages with a support/retry path; technical details stay server-side. Actual: English and potentially low-level exception text reaches the UI, causing confusion and possible infrastructure/path disclosure. | Map status/error codes to safe Vietnamese messages in the frontend; log a correlation ID server-side. Backend should stop putting raw exceptions in public `detail`. Document the backend hardening dependency instead of masking it with CSS. | Phase 1; backend dependency for complete remediation. |

### C. Navigation, UX, and responsive behavior

| ID | Severity | Route / state and source | Reproduction and evidence | Expected vs actual / impact | Technical cause and recommended direction | Blocks |
| --- | --- | --- | --- | --- | --- | --- |
| UI-NAV-001 | P1 | Knowledge list and authenticated history list. `KnowledgeList.tsx:70`; `HistoryList.tsx:145` | Browser DOM exposed knowledge headings but no buttons/links. Clicking the heading with a mouse opened detail. History row behaved the same; its arrow button had no accessible name. | Expected: every card/row action is a keyboard-focusable link or button with an accessible name and expanded state. Actual: core knowledge and history details are unavailable to keyboard users. | Render knowledge entries as semantic buttons or links. Render history expansion as one named button with `aria-expanded`/`aria-controls`; avoid a clickable parent plus nested unnamed button. | Phase 4/6. |
| UI-NAV-002 | P2 | Shell tabs, collapsed desktop sidebar, mobile/tablet navigation. `Sidebar.tsx:49`, `:131` | At 375/768, accessible tab names are `Chẩn đoán`, `Cơ`, and `Lịch` because labels are split on the first word. At collapsed desktop width, the two feature tabs had empty accessible names. Tabs have no `tabpanel`, `aria-controls`, IDs, or arrow-key behavior. | Expected: stable understandable labels and either complete tab semantics or ordinary navigation semantics. Actual: names change/disappear by viewport/collapse state and the ARIA tab contract is incomplete. | Prefer navigation buttons/links if these are app sections, or implement the full tabs pattern. Preserve full accessible names with visually shortened labels only when needed. Add tooltips to collapsed icons. | Phase 4/6. |
| UI-RESP-001 | P2 | Authenticated history at 375 px. `HistoryList.tsx:185` | A local prediction was created and loaded in history. Browser measured `confidenceVisible: false`; the list hides confidence below `sm`, and expanded details do not restore it. | Expected: confidence and prediction context remain available on mobile, possibly stacked or compact. Actual: a key trust signal disappears completely from mobile history. | Move confidence into the mobile row/subline or expanded content. Do not hide decision-critical information; change layout instead. | Phase 3. |
| UI-UX-001 | P2 | Authenticated empty history and unauthenticated history. `HistoryList.tsx:79`, `:119`; `page.tsx:219` | Empty authenticated history tells users to diagnose but has no action. Unauthenticated history repeats “Lịch sử chẩn đoán cá nhân” as both page heading and card title. | Expected: empty states provide the immediate next action and avoid repeated hierarchy. Actual: users must infer navigation; duplicate headings increase visual noise. | Extend `EmptyState` with optional action(s), route to a new diagnosis, and remove redundant card titles when the page heading already provides context. | Phase 3/4. |
| UI-VIS-002 | P2 | Desktop collapsed sidebar. `Sidebar.tsx:92`; `page.tsx:89` | At 1440 px, browser measured sidebar width 72 px but header/main still started at x=256 px because the shell always has `lg:pl-64`. | Expected: content offset follows sidebar width, or the collapsed sidebar overlays intentionally. Actual: 184 px of unused space remains and the layout feels broken. | Lift collapse state to the shell or expose it via context/CSS data attribute, then synchronize grid/offset transitions. | Phase 4. |
| UI-ROUTE-001 | P3 accepted exception | Knowledge/history/detail state on `/`. `page.tsx:33` | Click a tab/detail and reload or use browser history. Local state resets; there is no shareable URL. | URL-backed navigation would improve refresh/back behavior, but the project owner has explicitly prioritized a smaller academic-demo scope. | Accept ephemeral tab/detail state for this release. Do not add App Router routes or backend history-detail work; reconsider only if shareable links become a demonstrated requirement. | Closed by DEC-07; no implementation task. |
| UI-VIS-004 | P3 | Diagnosis empty state, especially 375 px. `page.tsx:103` | Browser measured a 48 px mobile heading wrapping to two lines and 60 px desktop heading. The desktop page has very large unused space while the primary upload control sits inside nested glass panels. No overflow occurred. | Expected: the upload task is visually dominant without excessive wrapping, nesting, or dead space. Actual: presentation is dramatic but less efficient, especially on smaller laptops and phones. | After functional repairs, tune fluid typography (`clamp`), vertical rhythm, and container nesting using the approved brand direction. This is polish, not a blocker. | Phase 3. |

### D. Visual consistency and design-system implementation

| ID | Severity | Route / state and source | Reproduction and evidence | Expected vs actual / impact | Technical cause and recommended direction | Blocks |
| --- | --- | --- | --- | --- | --- | --- |
| UI-VIS-001 | P2 | Auth modal, alerts, status colors, motion. `AuthModal.tsx:37`; `globals.css`; `tailwind.config.ts` | Mobile screenshots show no usable close control; in dark capture it overlapped the title. Built CSS search confirmed `animate-in`, `zoom-in-95`, `text-danger-400`, `bg-danger-900`, `text-warning-800`, `bg-warning-900`, `text-healthy-400`, and `bg-healthy-900` are missing. `top-4.5`/`right-4.5` also have no configured spacing utility. | Expected: every referenced utility compiles and state styling is consistent in both themes. Actual: placement, animation, and dark/status variants silently do nothing. This directly contributes to the broken auth appearance. | Replace invalid utilities with supported values or extend complete semantic token scales intentionally. Add a build-time/style test for critical classes and visually verify both themes. | Phase 1/3. |
| UI-VIS-003 | P3 | Global and feature components. `tailwind.config.ts`; `globals.css`; most components | Source mixes semantic tokens with `claude-*`, `stone-*`, `zinc-*`, `neutral-*`, arbitrary shadows, and partial `danger/warning/healthy` scales. | Expected: a small semantic vocabulary controls surfaces, text, border, accent, success, warning, danger, focus, and overlays. Actual: source/vendor naming and hard-coded palette utilities make light/dark behavior fragile and complicate future branding. | Keep Tailwind/CSS variables, rename toward brand-neutral semantic tokens, define complete required status/focus variants, and temporarily alias old names during incremental migration. | Phase 0 brand decision; Phase 3. |
| UI-ARCH-004 | P2 | Shared UI architecture. `page.tsx`, `Sidebar.tsx`, `AuthForm.tsx`, `BentoGrid.tsx`, `TabNav.tsx` | Repeated button/input/card class strings coexist with unused `TabNav`, unused `BentoGridItem` imports, `any` user/icon types, and a 244-line page that mixes shell and feature orchestration. | Expected: reusable semantic primitives and thin feature composition. Actual: fixes must be repeated and drift is already visible. | Use Radix only for Dialog/DropdownMenu behavior and add the smallest proven local wrappers: Button/IconButton, FormField, Pagination, Alert/Status, and EmptyState action. Remove dead code after usage search. Do not rewrite feature logic or add a pre-styled UI framework. | Phases 1–3. |

### E. Accessibility

| ID | Severity | Route / state and source | Reproduction and evidence | Expected vs actual / impact | Technical cause and recommended direction | Blocks |
| --- | --- | --- | --- | --- | --- | --- |
| UI-A11Y-001 | P2 | Icon buttons and interactive controls. `Header.tsx:29`; `HistoryList.tsx:192`, `:223`; `Sidebar.tsx:108`, `:186` | Browser found an unnamed 32x32 history expansion button; collapsed feature tabs had no name. Several controls use only `title`, and English labels such as “Expand sidebar”/“Remove file” are mixed into a Vietnamese UI. | Expected: every control has a stable Vietnamese accessible name and state. Actual: icon controls are silent, inconsistently named, or language-inconsistent. | Require `aria-label` for icon-only controls, use `aria-expanded` where applicable, and centralize labels in component props/content constants. | Phase 4/6. |
| UI-A11Y-002 | P2 | All routes, especially mobile. Multiple component utility strings | Browser measured 24 px modal close, 28 px upload/camera and sidebar collapse, 32 px submit/navigation, 34–38 px auth/theme controls. Many controls use `outline-none` with no `focus-visible` replacement. | Expected: approximately 44x44 px touch targets and a clearly visible keyboard focus indicator. Actual: touch and keyboard interaction is unnecessarily difficult. | Normalize Button/IconButton sizes, add `focus-visible` ring/offset tokens, and test keyboard order and touch targets at all viewports. | Phase 3/6. |
| UI-A11Y-003 | P2 | Loading, errors, prediction updates, all motion. `Animations.tsx`; `LoadingSpinner.tsx`; `ErrorMessage.tsx`; inline error blocks | Source has no `aria-live`, `role=status`, `role=alert`, or focus handoff for async results/errors. Framer Motion and spinners do not consult `prefers-reduced-motion`. | Expected: async status/result/error changes are announced, and nonessential motion is reduced when requested. Actual: visual state changes can be missed by assistive technology; motion always runs. | Add appropriate polite/assertive live regions, focus result/error headings when warranted, use Framer reduced-motion hooks/CSS media queries, and avoid repeated entrance animations on tab switches. | Phase 3. |
| UI-A11Y-004 | P3 | Sidebar/footer, headings, images. `globals.css`; `Sidebar.tsx:213`; `page.tsx:104`; image components | Token calculation found `text-tertiary` contrast at 2.56:1 on light background and 4.12:1 on dark, below 4.5:1 for normal text. Pages begin at `h2`; detail content can jump from `h2` to `h4`; image alt strings are generic English. | Expected: AA contrast for meaningful small text, one logical page heading, ordered headings, and localized useful alternatives. Actual: small metadata may fail contrast and document structure is inconsistent. | Remove internal footer text, raise any remaining tertiary contrast, define one `h1` per view/shell strategy, normalize heading levels, and localize alt text. Decorative icons should be hidden from assistive technology. | Phase 3. |

Verified accessibility defects above are based on rendered DOM, keyboard actions, measurements, and source. A specialized VoiceOver/NVDA pass is still required before claiming WCAG 2.2 AA conformance.

### F. Frontend architecture, environment safety, performance, and testing

| ID | Severity | Route / state and source | Reproduction and evidence | Expected vs actual / impact | Technical cause and recommended direction | Blocks |
| --- | --- | --- | --- | --- | --- | --- |
| UI-ARCH-001 | P1 | Host-run local frontend configuration. `frontend/.env.example:2`, `constants.ts:1`, `Dockerfile:14` | `.env.example`, the runtime fallback, and Dockerfile default all point to `https://plant-disease-demo.duckdns.org/api/v1`. Docker Compose correctly overrides to localhost, and this audit's `.env.local` was local. | Expected: local development fails closed or targets local API by default; production URL is supplied explicitly by deployment. Actual: `npm run dev` without a carefully edited local env can authenticate, upload, or create history against production. | Make `.env.example` local, remove the production runtime fallback or fail fast when unset, and require the production build/deploy pipeline to pass the public URL explicitly. Add an environment banner only in non-production if useful. | Phase 1 before broad UI testing. |
| UI-ARCH-002 | P2 | Diagnosis file preview/result. `ImageUploader.tsx:89`; `page.tsx:135` | Source calls `URL.createObjectURL` during render in two places and never calls `URL.revokeObjectURL`. The same file can create new URLs across re-renders. Build also warns about raw `<img>` in `page.tsx`. | Expected: one memoized object URL per file, revoked on change/unmount, and image sizing optimized without breaking local blob previews. Actual: repeated use can leak browser memory during iterative testing. | Introduce a small `useObjectUrl` hook or effect cleanup and share the URL across preview/result. Evaluate `next/image` only where it supports blob/remote requirements; otherwise document the intentional raw image. | Phase 3. |
| UI-ARCH-003 | P2 | All API-backed flows. `api.ts:88`, `useAuth.ts`, `HistoryList.tsx` | `handleResponse` returns `Promise<any>`, discards response status/code, joins validation structures into raw strings, and prevents reliable 401/409/413 handling. | Expected: typed success and error boundaries with status/code, safe message, field errors, and optional correlation ID. Actual: components parse only `Error.message`, producing inconsistent auth/error behavior. | Define `ApiError`, preserve HTTP status and structured validation details, map to localized UI copy at the boundary, and centralize unauthorized behavior. | Phase 1/2; backend codes optional but recommended. |
| UI-TEST-001 | P2 | Test suite. `frontend/src/lib/__tests__/api.test.ts`; `vitest.config.ts` | Repository search found only one test file. Runtime auth/navigation/upload/result/knowledge/history/accessibility behavior is untested. | Expected: critical flows have component and browser regression coverage. Actual: compilation and API mocks can pass while the confirmed modal, mobile logout, keyboard, and responsive defects remain. | Add RTL tests for auth/prediction/knowledge/history states and Playwright E2E for local-stack happy/error/auth flows at 375/768/1440. Add accessibility assertions and screenshot baselines only after UI foundations stabilize. | Tests accompany Phases 1–3 and are consolidated in Phase 4. |
| UI-TOOL-001 | P3 | Frontend scripts. `frontend/package.json:5` | `npm run lint` passes but Next reports `next lint` is deprecated and will be removed in Next 16. Type checking works only through an undocumented direct command; `tsc` generated incremental metadata when run. | Expected: stable explicit `lint`, `typecheck`, `test`, and `build` scripts usable locally and in CI without dirtying the tree. Actual: lint migration is pending and typecheck is not a package script. | Migrate to ESLint CLI, add `typecheck`, and send `.tsbuildinfo` to a cache/ignored location or disable incremental for the CI command. | Phase 4. |

## 7. Severity and impact matrix

| Priority | Issues | User impact | Delivery rule |
| --- | --- | --- | --- |
| P0 | None confirmed | None confirmed. | Stop release if later discovered. |
| P1 | UI-AUTH-001, UI-AUTH-002, UI-AUTH-003, UI-NAV-001, UI-ARCH-001 | Users can be trapped in sessions on mobile/tablet, critical auth/core knowledge paths are inaccessible, and local testing can accidentally target production. | Resolve before aesthetic redesign or production redeploy. |
| P2 | UI-AUTH-004, UI-FUNC-001, UI-FUNC-002, UI-FUNC-003, UI-CONTENT-001, UI-CONTENT-002, UI-TRUST-001, UI-ERROR-001, UI-NAV-002, UI-RESP-001, UI-UX-001, UI-VIS-001, UI-VIS-002, UI-ARCH-004, UI-A11Y-001, UI-A11Y-002, UI-A11Y-003, UI-ARCH-002, UI-ARCH-003, UI-TEST-001 | Significant trust, task completion, pagination, responsive, accessibility, error-recovery, and maintainability degradation. | Include in the planned remediation phases; do not defer merely because build passes. |
| P3 | UI-ROUTE-001, UI-VIS-003, UI-VIS-004, UI-A11Y-004, UI-TOOL-001 | Polish, consistency, accepted route limitation, semantic quality, and future upgrade cost. | Address in scoped phases; UI-ROUTE-001 is explicitly accepted by DEC-07. |

## 8. Screenshots and evidence references

### Retained screenshots

- [Mobile Login modal, 375x812](./ui-audit-evidence/mobile-auth-modal-375-full.jpg): confirms the modal fits vertically but the close control is not visibly positioned, internal “Studio” copy is present, and the background remains structurally active.
- [Mobile Registration modal, 375x812](./ui-audit-evidence/mobile-register-modal-375-full.jpg): confirms registration fits the viewport but shares the missing close control, internal copy, compact controls, and weak modal separation.

### Browser and command evidence

- 375, 768, and 1440 px DOM measurements: no horizontal document overflow was detected.
- 375/768 px authenticated shell: zero visible logout controls.
- 1440 px collapsed shell: sidebar width 72 px; header/main x-position 256 px.
- Auth overlay: zero dialog elements, zero `aria-modal`, focus remained on opener, Escape did not close, inputs had zero associated labels.
- Mobile upload: click-only prompt had `tabIndex=-1`, no role; action controls measured 28, 28, and 32 px high.
- Mobile authenticated history: confidence was absent; expansion button was unnamed.
- Unknown route: default English 404 rendered under Vietnamese document language.
- Browser console: no warning/error entries captured for the exercised flows.
- Local backend logs confirmed successful auth, predict, knowledge/history requests; no 5xx occurred during the audit.
- Compiled CSS search confirmed the missing utility/status classes listed in UI-VIS-001.
- Contrast calculations: light tertiary/white 2.56:1; dark tertiary/dark background 4.12:1; normal body/muted tokens otherwise met the sampled AA thresholds.

## 9. Proposed design principles

1. **Diagnosis first:** every screen should make the next safe action obvious, with one primary action and minimal technical noise.
2. **Trust without overclaiming:** call outputs predictions, show uncertainty and alternatives, keep advisories visible, and separate model output from verified agronomic guidance.
3. **Vietnamese by default:** user-facing labels, errors, accessible names, empty states, and not-found content use consistent natural Vietnamese. English disease names may remain secondary scientific/reference content.
4. **Responsive parity:** mobile/tablet may rearrange content but must not remove account control, confidence, context, or recovery actions.
5. **Semantic before decorative:** buttons, dialogs, forms, navigation, status messages, and headings must work without a mouse before motion/glass/shadow polish is applied.
6. **Environment-safe development:** local UI work must never contact production implicitly.
7. **Existing stack, incremental change:** retain Next.js, Tailwind, local fetch integration, Lucide, and current feature components unless a measured defect requires change.
8. **Small reusable contracts:** create only primitives that remove repeated defects; keep business and API behavior in hooks/services rather than presentation components.

## 10. Proposed component and design-token strategy

### Components to normalize

- `Button` and `IconButton`: thin local wrappers using existing `clsx`/`tailwind-merge`; variants, disabled/loading states, 44 px target option, focus-visible treatment, and accessible-name requirement.
- `Dialog`: a small styled wrapper around Radix Dialog. Reuse its Portal, Overlay, Content, Title, Description, Close, focus trapping, Escape handling, and focus restoration instead of maintaining custom modal behavior.
- `AccountMenu`: a styled wrapper around Radix DropdownMenu, shared by desktop and mobile/tablet account controls. Logout is a labelled menu item, not a floating icon beside the username.
- `FormField`: label/input association, description, validation message, `aria-invalid`, autocomplete, and disabled state.
- `Alert`/`Status`: semantic error, warning, success, and loading announcements.
- `Surface`/`Card`: one level of visual containment with consistent radius, border, and shadow.
- `SectionNavigation`: full accessible labels and either proper navigation or complete tab semantics.
- `EmptyState`: optional primary/secondary actions.
- `Pagination`: a small project-specific composite because Radix does not provide a pagination primitive; reuse Button/IconButton, expose current page/total pages, and guard transitions while loading.
- `PredictionTrustSummary`: disease name, confidence, uncertainty note, and disclaimer as one consistent unit across result and history.

Do not add a pre-styled component framework or copy a large generated component set into the repository. Radix is intentionally unstyled and incrementally adoptable, so existing Tailwind tokens remain the visual source of truth while the library owns difficult interaction behavior. Use Lucide for all icons; do not add a second icon library.

### Token migration

Keep CSS variables and Tailwind. Add/normalize semantic tokens for:

- `background`, `surface`, `surface-raised`, `overlay`;
- `text-primary`, `text-secondary`, `text-tertiary` with AA-safe values;
- `border`, `border-strong`, `focus-ring`;
- `accent`, `accent-hover`, `accent-foreground` after branding approval;
- complete `success`, `warning`, `danger`, and `info` foreground/background/border combinations;
- spacing/radius/shadow aliases only where repeated.

Temporarily alias `claude-*` tokens to the new semantic names, migrate usages incrementally, then remove the aliases. Do not introduce a new UI framework or wholesale theme package.

## 11. Authentication UI remediation plan

1. Keep auth modal-only and migrate `AuthModal` to the shared Radix Dialog wrapper.
2. Give the modal header an explicit grid/flex layout with title content and a 44x44 px `Dialog.Close`; do not use unsupported `top-4.5`/`right-4.5` positioning.
3. Rename “Tài khoản Studio” and remove unsupported account-tier copy.
4. Bind labels, add autocomplete (`username`, `email`, `current-password`, `new-password` as appropriate), reveal/hide password control if approved, and associate field/server errors.
5. Translate known 401/409/422 messages; preserve HTTP status in `ApiError`.
6. Add the shared Radix AccountMenu to mobile/tablet and desktop. Constrain long usernames and keep logout inside the menu so it cannot overlap account content.
7. Handle expired sessions centrally: clear the existing `localStorage` token, show a localized explanation, and reopen Login when the user chooses to continue.
8. Retain automatic login after registration; close the modal only after `/me` succeeds and show a clear failure state otherwise.
9. Do not add forgot-password/reset UI or backend work.
10. Keep JWT storage unchanged; cookie migration is not part of this plan.

## 12. Internal-content and information-exposure cleanup plan

- Remove `v1.2.0`, `Claude UI`, `Studio`, `Dashboard`, and `Thành viên Free` unless a product owner explicitly approves a replacement use.
- Decide the public product name; use it consistently in metadata, shell, favicon treatment, and documentation.
- Replace “Chẩn đoán chính xác nhất” with calibrated prediction language.
- Replace “Tư vấn kỹ thuật chuyên nghiệp” unless the content is actually reviewed/owned by qualified experts and that claim is approved.
- Hide prediction UUID and raw model label; retain labelled latency as the model-response metric for academic evaluation.
- Convert backend technical errors to safe localized messages; keep raw exceptions in server logs.
- Keep sources visible and add a consistent baseline advisory, not only record-dependent advisory text.
- Do not expose environment names or internal URLs in rendered UI. A development-only environment marker may be shown only when `NODE_ENV !== production` and must not contain secrets.

## 13. Responsive-design improvement plan

### Mobile (~375 px)

- Preserve account/logout through a compact user menu or fourth navigation action.
- Use full accessible navigation names while allowing concise visible labels.
- Reduce hero type/vertical spacing so the upload action remains clearly above the bottom navigation.
- Keep confidence in history; stack it below the result name/date.
- Use 44 px controls and safe-area padding for the fixed bottom navigation.
- Ensure dialogs use `max-height`, internal scrolling when necessary, and a visible close action.
- Stack result cards and recommendation sections without nested surface padding.

### Tablet (~768 px)

- Do not treat the full tablet range as a phone without evaluating navigation space. At minimum, provide the same account/session controls as desktop.
- Use a two-column result layout only when each column remains readable; otherwise keep a stacked trust-first sequence.
- Use the available width for full navigation labels and clearer empty states.

### Desktop (~1440 px)

- Synchronize collapsed sidebar width and shell offset.
- Keep the primary diagnosis surface within a readable working width without excessive empty canvas.
- Ensure collapsed navigation icons retain names/tooltips and auth remains reachable.
- Verify 1024–1280 px separately because that is where the shell changes from bottom navigation to sidebar.

Across all widths, retain the confirmed no-horizontal-overflow behavior and add tests for loading-to-loaded layout shift.

## 14. Accessibility improvement plan

- Use WCAG 2.2 AA as practical guidance for the repaired critical interactions; this academic-demo plan does not claim formal conformance.
- Use Radix Dialog/DropdownMenu behavior and complete semantic FormField, navigation/tabs, disclosure, status, and alert patterns.
- Provide visible focus and logical keyboard order; test Escape, Tab, Shift+Tab, Enter, Space, and arrow keys where a tabs pattern is retained.
- Make all actionable cards and rows semantic controls.
- Enforce 44x44 px touch targets for primary and icon controls where practical.
- Add `aria-live`/status behavior for prediction loading/success/error and auth errors.
- Normalize heading hierarchy and localized accessible names/alt text.
- Fix sampled contrast failures and validate both themes with automated and manual checks.
- Respect reduced motion in Framer Motion and CSS; keep content immediately available when motion is reduced.
- Run a macOS VoiceOver smoke pass when available; NVDA/Narrator, real-device safe-area/camera, and formal audit work are best-effort rather than demo blockers.
- Verify keyboard-only behavior and 200% zoom for the critical flows in the primary Chromium target.

## 15. Frontend test and browser-verification strategy

### Unit and component tests

- Keep API client tests, but assert typed `ApiError` status/code behavior.
- Add React Testing Library coverage for:
  - Login/Register labels, validation, loading, success, 401/409, and mode switching.
  - Dialog focus, Escape, focus restoration, and accessible naming.
  - Mobile/desktop account/logout rendering.
  - New diagnosis reset.
  - Knowledge card keyboard activation.
  - History empty/list/expanded, confidence preservation, pagination, and unauthorized recovery.
  - Prediction confidence/top-k/disclaimer semantics.
- Add automated accessibility assertions to critical component states.

### Browser/E2E tests

- Add a Playwright project using the local stack and isolated test account/data.
- Cover 375x812, 768x900, and 1440x1000.
- Test register -> authenticated shell -> predict -> saved history -> logout -> login.
- Test invalid file, oversized file, backend validation error, 401 expiration, 409 registration conflict, knowledge retry, and not-found recovery.
- Assert no horizontal overflow, usable targets, visible focus, dialog focus trap, and reduced-motion mode.
- Run light and dark themes and capture visual baselines only after token/component stabilization.
- Keep production smoke tests read-only except for a separately approved dedicated test account. Never reuse local E2E defaults against production.

### Required gates after implementation

```bash
cd frontend
npm ci
npm run lint
npm run typecheck
npm test
npm run build
npx playwright test
```

## 16. Phased implementation roadmap

### Phase 0: Freeze the academic-demo scope and UI dependency boundary

**Objective:** Prevent scope creep before implementation starts.

**Included issues:** Decision baseline in Section 4.1, UI-ARCH-004, and UI-TRUST-001 wording.

**Likely files:** this plan, `frontend/package.json`, `frontend/package-lock.json`, optional short frontend UI conventions note.

**Tasks:** record the academic-demo constraints; retain modal auth, `localStorage` JWT, and local-state tabs; explicitly exclude password reset, HttpOnly cookies, deep-link routing, and backend history-detail work; approve `PlantDisease AI` and the prediction/disclaimer copy; add the tree-shakeable `radix-ui` dependency without Radix Themes and document its allowed primitives (`Dialog`, `DropdownMenu`).

**Dependencies:** Project owner approval of the wording and package addition.

**Risks:** Importing the umbrella package carelessly or mixing Radix styles with a second theme system can increase bundle/style complexity. Import only used primitives and measure the production bundle.

**Validation:** `npm install` produces one intentional dependency change; build succeeds; bundle output is recorded; plan exclusions remain explicit.

**Acceptance criteria:** Scope and dependency choices are fixed, no backend change is required, and implementation can begin without unresolved auth/routing/security questions.

**Suggested commits:** `docs(ui): scope academic demo improvements and component strategy`; dependency installation may be included with the first component commit instead of a dependency-only commit.

### Phase 1: Fix demo-blocking interactions

**Objective:** Repair the defects the user encounters before visual polish.

**Included issues:** UI-FUNC-001, UI-FUNC-003, UI-AUTH-001, UI-AUTH-002, UI-VIS-001, and UI-ARCH-001.

**Likely files:** `frontend/package.json`, `frontend/src/app/page.tsx`, `usePrediction.ts`, `AuthModal.tsx`, `Sidebar.tsx`, `HistoryList.tsx`, new `components/ui/Dialog.tsx`, `AccountMenu.tsx`, `Button.tsx`, `Pagination.tsx`, frontend environment files, and focused tests.

**Tasks:** expose `handleReset` from `usePrediction` to `page.tsx`; create `startNewDiagnosis` that resets file/result/error/loading and returns to diagnosis; replace the auth overlay with Radix Dialog and reserve close-button space; replace the cramped logout icon with a Radix DropdownMenu account action at all widths; extract and finish pagination with labelled controls and loading/boundary behavior; replace invalid Tailwind utilities; keep local API configuration fail-safe.

**Dependencies:** Phase 0 dependency choice; current backend history pagination contract already supports `page` and `page_size`.

**Risks:** A reset during an in-flight request can allow a late response to repopulate stale results. Disable reset while submitting or cancel/ignore stale requests. Account/menu portals must layer above the fixed shell and bottom navigation.

**Validation:** component tests for reset, Dialog close/Escape/focus, long-username account menu, logout, and 1/2/3-page history fixtures; browser checks at 375/768/1440; local network requests never target production; build contains all referenced classes.

**Acceptance criteria:** “Chẩn đoán mới” always returns to a clean upload state; Login/Register close never overlaps content; logout is reachable and non-overlapping at every target width; history with 11 fixtures can navigate pages 1–3 correctly; no local request silently targets production.

**Suggested commits:** (1) `fix(diagnosis): reset state for new diagnosis`; (2) `refactor(ui): add radix dialog and account menu`; (3) `fix(auth): repair modal close and responsive logout`; (4) `fix(history): complete reusable pagination`; (5) targeted regression tests.

### Phase 2: Repair Login, Registration, and authentication states

**Objective:** Make the complete auth lifecycle predictable and accessible at every viewport.

**Included issues:** UI-AUTH-001, UI-AUTH-002, UI-AUTH-003, UI-AUTH-004.

**Likely files:** `AuthModal.tsx`, `AuthForm.tsx`, `useAuth.ts`, `api.ts`, `Sidebar.tsx`, and the Phase 1 Dialog/FormField/AccountMenu wrappers.

**Tasks:** field/error association; localized errors; loading/success states; autocomplete; preserve automatic login after registration; centralize 401 handling; clear stale `localStorage` state; verify the shared account/logout menu. Do not add auth routes, password reset, verification, cookie migration, roles, or account tiers.

**Dependencies:** Phase 1 Radix wrappers and typed API errors; no backend schema change.

**Risks:** Focus management regressions; accidentally changing auth business behavior; mobile menu layering with bottom navigation.

**Validation:** keyboard-only register/login/logout; Dialog focus/Escape/restore; 401/409 tests; long username; 375/768/1440 browser checks; no background interaction while the modal or account menu is open.

**Acceptance criteria:** All P1 auth findings pass component and browser tests; logout is reachable at all widths; errors are localized and associated.

**Suggested commits:** (1) `refactor(api): preserve status for localized auth errors`; (2) `fix(auth): repair form and session states`; (3) auth component/browser tests.

### Phase 3: Apply focused visual, responsive, and content improvements

**Objective:** Make the demo coherent and usable without a broad redesign or feature rewrite.

**Included issues:** UI-CONTENT-001/002, UI-TRUST-001, UI-ERROR-001, UI-NAV-001/002, UI-RESP-001, UI-VIS-002/003/004, UI-UX-001, UI-ARCH-002/003/004, and scoped accessibility findings.

**Likely files:** `globals.css`, `tailwind.config.ts`, `page.tsx`, `Header.tsx`, `Sidebar.tsx`, `PredictionResult.tsx`, `TopKList.tsx`, `RecommendationCard.tsx`, `HistoryList.tsx`, `KnowledgeList.tsx`, `ImageUploader.tsx`, existing/new small `components/ui/*`, and API/error utilities.

**Tasks:** remove `v1.2.0`, `Claude UI`, `Studio`, `Dashboard`, and unsupported tier copy; hide raw label/ID while retaining labelled latency for academic model-performance evaluation; apply the agreed prediction/confidence/disclaimer wording; normalize only repeated semantic tokens; fix sidebar collapse offset; preserve confidence on mobile; give empty states actions; make cards/history rows semantic; fix object-URL lifecycle; improve focus, labels, contrast, live status, reduced motion, touch targets, and 375/768/1440 layouts. Keep tabs as local state and avoid route/backend expansion.

**Dependencies:** Stable Phase 1–2 interactions and agreed content from Section 4.1.

**Risks:** Large styling sweeps can create dark-mode regressions or obscure feature behavior. Migrate one feature group at a time and retain token aliases until every usage is checked.

**Validation:** component tests beside each changed feature; light/dark browser matrix at 375/768/1440; keyboard pass; no overflow; compiled-class search; object-URL cleanup test; no console errors.

**Acceptance criteria:** No internal labels or technical prediction metadata remain in normal UI; core actions and confidence remain visible at all target widths; meaningful controls have names/focus; shell collapse and empty states behave correctly; no new route or backend endpoint is introduced.

**Suggested commits:** (1) content/trust cleanup; (2) shared tokens/buttons/status; (3) diagnosis/result UI; (4) shell/responsive layout; (5) knowledge/history semantics and empty states; tests accompany each group.

### Phase 4: Regression and deployment handoff

**Objective:** Prove the improved demo works end to end on the full local stack before a teammate deploys it.

**Included issues:** UI-TEST-001, UI-TOOL-001, all repaired P1/P2 demo-scope findings, and remaining accepted P3 polish.

**Likely files:** `package.json`, ESLint config, Vitest/React Testing Library tests, Playwright config/tests, evidence documentation, and only small regression fixes.

**Tasks:** add explicit `typecheck` and stable lint scripts; consolidate component tests; add Playwright local-stack flows for auth, reset, prediction, multi-page history, knowledge, logout, errors, and themes; verify API target; run production build; prepare a concise teammate deployment/smoke checklist. Use mocked data for pagination/presentation plus one real local prediction; do not create production data during this task.

**Dependencies:** Stable Phases 1–3 and the existing local Docker stack/model artifact.

**Risks:** Real inference and shared database state can make E2E flaky. Keep most presentation tests deterministic and isolate the single real-stack smoke record/account.

**Validation:** `lint`, `typecheck`, unit/component tests, build, and Playwright pass from a clean dependency install; browser console has no errors; requests target local services; manual 375/768/1440 and light/dark checks pass.

**Acceptance criteria:** All P1 and selected demo-scope P2 issues pass tests; reset/auth/logout/pagination work end to end; no horizontal overflow or blocked primary action; production build succeeds; deployment and rollback/smoke steps are documented for the teammate.

**Suggested commits:** (1) tooling scripts; (2) component regression suite; (3) Playwright local-stack flows; (4) final evidence/docs and narrowly scoped regressions.

## 17. Dependencies and risks

| Dependency/risk | Why it matters | Mitigation |
| --- | --- | --- |
| Branding/product naming | Current UI contains no approved public identity and leaks “Claude UI/Studio”. | Resolve Phase 0 before token/copy polish. |
| Backend error contract | Raw exception details and English auth errors cannot be fully solved by styling. | Introduce safe frontend mapping now; request stable backend error codes and non-raw public details. |
| Radix adoption | A new UI dependency can become a second design system if themes or unused primitives are added broadly. | Use unstyled primitives only, initially Dialog and DropdownMenu; keep Tailwind tokens and Lucide; measure the build and avoid generated component collections. |
| Auth storage | JWT `localStorage` is an accepted academic-demo constraint. | Keep behavior unchanged except reliable logout/401 cleanup; do not create a cookie-migration task in this plan. |
| Forgot/reset password | No backend endpoint exists and the feature is excluded. | Do not render a dead link or add frontend/backend recovery work. |
| Model semantics | Confidence may not be calibrated probability; no segmentation geometry is returned. | Use “confidence/prediction” language, do not invent overlays, confirm calibration language with ML owner. |
| Production API fallback | Local development can accidentally target production. | Fix first; add environment tests and explicit deploy-time injection. |
| Visual baseline absence | There is no Figma/Storybook/brand reference. | Establish minimal approved guidelines and use evidence-backed changes rather than aesthetic preference. |
| Test data/inference cost | E2E prediction writes MinIO/Postgres and inference is slower/non-deterministic. | Dedicated local test account, cleanup strategy, mocked presentation tests, one real-stack smoke case. |
| Dark/light token gaps | Partial color scales already compile inconsistently. | Token inventory and compiled-CSS verification before mass migration. |
| Browser/device coverage | In-app Browser cannot replace real camera, safe-area, and screen-reader testing. | Make Chromium plus 375/768/1440 the demo gate; record Firefox/Safari/device/assistive-technology checks as best-effort evidence. |

## 18. Acceptance criteria for each phase

The phase-specific criteria are embedded in Section 16. Release-level criteria are:

- All P1 findings are closed before visual redesign is considered complete.
- Demo-scope P2 findings in Phases 1–4 are closed; deferred route/security/product-hardening items remain explicitly accepted or excluded.
- Local development cannot silently call production.
- Login, registration, session expiration, account display, and logout work at 375, 768, and 1440 px.
- Diagnosis upload/loading/success/error/reset and authenticated history persistence pass automated and manual checks.
- History pagination is verified with at least 11 deterministic records across three pages, including first/last/loading/error boundaries.
- Knowledge and history core tasks work with keyboard only.
- No user-facing `Claude UI`, unsupported tier, raw exception, internal ID, or unapproved version string remains.
- Prediction language and disclaimer are approved by product/ML/domain owners.
- Light/dark meaningful text and controls meet sampled WCAG AA contrast guidance; all critical controls have visible focus and accessible names.
- No horizontal overflow or critical content loss occurs at supported widths.
- `lint`, `typecheck`, unit/component tests, build, and E2E tests pass from a clean working tree.
- Production deployment receives the intended API URL explicitly and passes a non-destructive smoke test.
- No `/login`, `/register`, password-reset, HttpOnly-cookie, deep-link, or history-detail backend work is introduced by this scope.

## 19. Recommended commit breakdown

Keep commits reviewable and behavior-focused. A recommended sequence is:

1. `docs(ui): scope academic demo improvements and component strategy`
2. `fix(frontend): isolate local and production API configuration`
3. `fix(diagnosis): reset state for new diagnosis`
4. `refactor(ui): add radix dialog account menu and shared controls`
5. `fix(auth): repair modal form session and responsive logout`
6. `fix(history): complete reusable pagination`
7. `fix(ui): remove internal metadata and calibrate prediction copy`
8. `fix(ui): improve shell result knowledge and responsive states`
9. `test(frontend): cover reset auth pagination and critical UI states`
10. `test(e2e): verify local demo flows and target viewports`
11. `chore(frontend): finalize quality gates and demo handoff evidence`

Avoid a single “redesign everything” commit. Do not mix backend public-error hardening into unrelated visual commits; use a clearly scoped backend commit/PR if approved.

## 20. Open questions requiring human decisions

The product, auth, routing, security, metadata, component-library, browser, and accessibility scope questions are resolved in Section 4.1. Only these items remain outside the UI implementation team's authority:

1. Should anonymous predictions continue to upload/store images, and what retention/privacy notice should the demo show?
2. Is there an approved production smoke-test account and cleanup policy after the teammate deploys the branch?
3. Who gives the final visual approval in the absence of Figma/brand documentation?
