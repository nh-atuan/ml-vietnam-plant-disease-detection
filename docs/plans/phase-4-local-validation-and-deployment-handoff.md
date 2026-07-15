# Phase 4 local validation and deployment handoff

## Local prerequisites

- Docker Desktop and Docker Compose
- Node.js/npm for host-run frontend checks
- Local model artifact and local environment values already configured by the project owner

## Commands

```bash
docker compose up --build -d
cd frontend
npm ci
npm run lint
npm run typecheck
npm test
npm run build
```

For a source frontend while Docker owns port 3000:

```bash
cd frontend
npm run dev -- --port 3001
```

## Non-destructive smoke checklist

1. Confirm the frontend is using the local API, not a production endpoint.
2. At 375, 768, and 1440 px, open Diagnosis, Knowledge, History, Login, and AccountMenu.
3. Verify Login/Register validation, Escape/close focus restoration, logout, and expired-session UI.
4. Verify “Chẩn đoán mới” clears an existing result.
5. Verify History pagination with at least 11 local records and its empty-state CTA.
6. Verify localized prediction/top-k names, latency, and absence of raw label/ID/internal product copy.
7. Check light/dark mode, keyboard interaction, console errors, and failed network requests.

## Deployment handoff

1. Teammate reviews the working-tree diff and runs all commands above.
2. Deploy with the intended production API URL supplied explicitly by the deployment environment.
3. Run the same smoke checklist using a non-production test account where available.
4. If a critical regression occurs, roll back to the previously deployed frontend image/revision and retain browser/network evidence for diagnosis.

## Excluded scope and limitations

- No backend/model/API-schema changes, password reset, HttpOnly-cookie migration, auth routes, or deep links.
- JWT localStorage remains an accepted academic-demo constraint.
- WCAG guidance is not a formal conformance certification.
- Raw `img` remains intentional for local blob previews because Next Image does not directly cover object URLs.
