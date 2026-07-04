## ADDED Requirements

### Requirement: API base URL configuration
The frontend SHALL read the backend API base URL from `NEXT_PUBLIC_API_BASE_URL` and MUST fall back to `http://localhost:8000/api/v1` when the variable is absent.

#### Scenario: Local default API URL
- **WHEN** the frontend runs without `NEXT_PUBLIC_API_BASE_URL`
- **THEN** API requests target `http://localhost:8000/api/v1`

#### Scenario: Deployment API URL override
- **WHEN** `NEXT_PUBLIC_API_BASE_URL` is set
- **THEN** API requests target the configured value without hard-coded localhost assumptions

### Requirement: Typed backend API client
The frontend SHALL provide typed client functions for prediction, knowledge, authentication, current-user lookup, and history endpoints in `frontend/src/lib/api.ts`, with TypeScript types matching backend Pydantic schemas.

#### Scenario: Prediction response includes all backend fields
- **WHEN** `/api/v1/predict` returns a response
- **THEN** the frontend type includes `prediction`, `confidence`, `top_k`, `recommendation`, `image_id`, `image_url`, `prediction_id`, and `latency_ms`

#### Scenario: Auth and history types match backend schemas
- **WHEN** the API client defines auth and history types
- **THEN** `TokenResponse` includes `access_token` and `token_type`, `HistoryResponse` includes `items`, `total`, `page`, and `page_size`, and `UserResponse` includes `id`, `username`, `email`, `is_active`, and `created_at`

#### Scenario: API error detail is surfaced
- **WHEN** a backend request fails with a JSON `detail` message
- **THEN** the frontend surfaces that message in a user-visible error state instead of a generic failure

### Requirement: Image input and validation
The frontend SHALL allow users to select, drag and drop, or capture a leaf image for diagnosis, and MUST validate file type and size before upload.

#### Scenario: Supported image is accepted
- **WHEN** the user selects a jpeg, png, or webp image no larger than 10 MB
- **THEN** the frontend shows a preview with filename and size, and enables prediction submission

#### Scenario: Unsupported file is rejected
- **WHEN** the user selects a non-image file or unsupported image type
- **THEN** the frontend prevents submission and shows that only jpeg, png, or webp images are supported

#### Scenario: Oversized image is rejected
- **WHEN** the user selects an image larger than 10 MB
- **THEN** the frontend prevents submission and explains the 10 MB limit before calling the backend

#### Scenario: Image is preserved on prediction failure
- **WHEN** a prediction request fails
- **THEN** the selected image remains in the preview so the user can retry without reselecting

### Requirement: Prediction submission
The frontend SHALL submit valid images to `POST /api/v1/predict` as `multipart/form-data` with form field named `file`.

#### Scenario: Anonymous prediction
- **WHEN** an unauthenticated user submits a valid image
- **THEN** the frontend sends the file without an authorization header and renders the diagnosis

#### Scenario: Authenticated prediction
- **WHEN** an authenticated user submits a valid image
- **THEN** the frontend includes `Authorization: Bearer <token>` so the backend associates the prediction with history

#### Scenario: Loading state during prediction
- **WHEN** the prediction request is in progress
- **THEN** the frontend disables duplicate submission and shows a loading indicator

### Requirement: Prediction result with trust signals
The frontend SHALL display the diagnosis result with confidence and top-k as prominent trust signals.

#### Scenario: Primary result display
- **WHEN** prediction succeeds
- **THEN** the frontend shows Vietnamese disease name (from recommendation.name_vi when available), model label, confidence percentage, and prediction latency

#### Scenario: Confidence is prominent
- **WHEN** prediction succeeds with `confidence`
- **THEN** the confidence is displayed as a large percentage with "Độ tin cậy" label, and `recommendation.confidence_note` is shown when available

#### Scenario: Top-k with visual comparison
- **WHEN** prediction succeeds with `top_k`
- **THEN** the frontend shows ranked alternatives with labels, confidence values, and proportional confidence bars

#### Scenario: Close predictions trigger caution
- **WHEN** the top-1 and top-2 confidence gap is less than 10%
- **THEN** the frontend shows caution text advising the user to compare symptoms or retake a clearer image

#### Scenario: No fake segmentation
- **WHEN** the backend response does not include masks or boxes
- **THEN** the frontend does not render segmentation overlays

### Requirement: Vietnamese expert recommendation
The frontend SHALL render the `recommendation` object in a readable format for Vietnamese users.

#### Scenario: Recommendation available
- **WHEN** prediction response includes a recommendation
- **THEN** the frontend shows description, symptoms, causes, treatments, prevention, severity, confidence note, advisory, and source links where provided

#### Scenario: Recommendation missing
- **WHEN** prediction response has no recommendation
- **THEN** the frontend shows the model result and states that expert guidance is unavailable for that label

### Requirement: Tab navigation
The frontend SHALL provide client-side tab navigation within a single page for three sections: diagnosis, knowledge, and history.

#### Scenario: Default tab
- **WHEN** the app loads
- **THEN** the diagnosis tab is active and the upload/result UI is visible

#### Scenario: Tab switching
- **WHEN** the user clicks a different tab
- **THEN** the corresponding panel renders without a page reload

#### Scenario: History tab requires auth
- **WHEN** an unauthenticated user clicks the history tab
- **THEN** the history panel prompts for login instead of making an unauthenticated API call

### Requirement: Authentication flow
The frontend SHALL support the backend JWT auth flow with register, login, token persistence, user restore, and logout.

#### Scenario: User registration
- **WHEN** a user submits username, email, and password
- **THEN** the frontend calls `POST /api/v1/auth/register` and shows success or validation errors

#### Scenario: User login
- **WHEN** a user submits valid credentials
- **THEN** the frontend calls `POST /api/v1/auth/login`, stores the token in localStorage, and updates UI to authenticated state

#### Scenario: User restore on page load
- **WHEN** a token exists in localStorage on mount
- **THEN** the frontend calls `GET /api/v1/auth/me` to restore user state, or clears the token if invalid

#### Scenario: Logout
- **WHEN** the user logs out
- **THEN** the token and user state are cleared without affecting anonymous diagnosis

### Requirement: Prediction history
The frontend SHALL allow authenticated users to view prediction history from `GET /api/v1/history`.

#### Scenario: History list loaded
- **WHEN** an authenticated user views the history tab
- **THEN** the frontend displays paginated items with predicted label, confidence, image URL, and created time

#### Scenario: Empty history
- **WHEN** history returns zero items
- **THEN** the frontend shows an empty state directing the user to start diagnosing

#### Scenario: Unauthenticated history
- **WHEN** an unauthenticated user views the history tab
- **THEN** the frontend prompts for login

### Requirement: Knowledge browsing
The frontend SHALL include a knowledge browser for supported diseases from `/api/v1/knowledge` and `/api/v1/knowledge/{disease_label}`.

#### Scenario: Disease list
- **WHEN** the knowledge tab loads
- **THEN** the frontend displays supported disease labels with Vietnamese name, English name, crop, and severity

#### Scenario: Disease detail
- **WHEN** the user selects a disease label
- **THEN** the frontend loads and displays symptoms, causes, treatments, prevention, and source links

#### Scenario: Knowledge independent of prediction
- **WHEN** no prediction has been submitted
- **THEN** the knowledge browser is still accessible and functional

### Requirement: Mobile-first responsive UI
The frontend SHALL provide a mobile-first layout usable on phone, tablet, and desktop widths.

#### Scenario: Mobile diagnosis flow
- **WHEN** viewed on a mobile-width screen
- **THEN** upload controls, submit action, result, and recommendations are readable without horizontal scrolling

#### Scenario: Desktop workspace
- **WHEN** viewed on a desktop-width screen
- **THEN** image/result and recommendation panels use available space in a grid layout

### Requirement: Accessible and polished UI states
The frontend SHALL include accessible labels, keyboard focus, loading/error/empty states, and a balanced visual system.

#### Scenario: Keyboard navigation
- **WHEN** a user navigates the diagnosis flow by keyboard
- **THEN** file input, submit, auth controls, tab navigation, and retry actions have visible focus and understandable labels

#### Scenario: Backend service unavailable
- **WHEN** prediction fails because the backend is unavailable
- **THEN** the frontend shows a recoverable error state with the backend detail message and does not discard the selected image

#### Scenario: Visual system
- **WHEN** the frontend is implemented
- **THEN** it uses semantic colors (healthy/warning/danger/info) beyond one-note green, with stable element dimensions across viewports

### Requirement: Build and test verification
The frontend SHALL pass build verification and include Vitest tests for the API client.

#### Scenario: Build passes
- **WHEN** `npm run build` is executed
- **THEN** the build completes without type or compile errors

#### Scenario: API client tests
- **WHEN** Vitest runs
- **THEN** tests verify prediction request/response, auth header injection, error message extraction, and file validation logic
