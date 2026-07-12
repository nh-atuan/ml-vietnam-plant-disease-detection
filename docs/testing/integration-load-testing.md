# Phase 6.6 — Integration and Load Testing Report

## Scope and acceptance criteria

This report covers the assigned Phase 6.6 flow:

`register/login -> upload leaf image -> prediction -> history`

The automated E2E test uses the real FastAPI routes, authentication, request validation, SQLModel persistence, and history query. ONNX Runtime and MinIO are deterministic test doubles so the test is repeatable in CI without a model artifact or external object store.

## Automated integration result

Run from the repository root:

```powershell
$env:PYTHONPATH='.'
.\.venv\Scripts\python.exe -m pytest -q tests/integration
```

Expected result: `2 passed`. The first test verifies the complete authenticated flow and response contract; the second verifies that history remains protected. The repository CI discovers this suite through `pytest -q tests`; it installs Helm so the existing chart checks do not prevent the integration tests from running.

Latest repository validation (2026-07-12): `2 passed` for this E2E suite. With the temporary-directory permission issue isolated and remote checks disabled, the remaining non-Helm suite completed with `33 passed`. The existing Helm-only checks were not run because the local machine has no `helm` executable.

## Load-test scenario

`tests/load/locustfile.py` simulates authenticated API clients. Its weighted traffic is:

| Endpoint | Weight | Purpose |
| --- | ---: | --- |
| `/health` | 4 | Liveness and ingress path |
| `/api/v1/history` | 3 | Authenticated database read |
| `/api/v1/knowledge` | 2 | Knowledge-base read |
| `/api/v1/predict` | 1 | Upload and inference path, only when an image is supplied |

Prerequisites: a dedicated non-production test account and a representative JPEG/PNG leaf image. Do not run the load test against production with personal credentials or without approval.

```powershell
$env:LOCUST_USERNAME='load_test_user'
$env:LOCUST_PASSWORD='replace-with-test-password'
$env:LOCUST_IMAGE_PATH='C:\path\to\representative-leaf.jpg'
.\.venv\Scripts\locust.exe -f tests\load\locustfile.py --host https://plant-disease-demo.duckdns.org --headless -u 5 -r 1 -t 2m --html reports\phase6-locust.html --csv reports\phase6-locust
```

Start with five users for two minutes. Record the generated HTML/CSV files as run evidence; they are intentionally ignored because they contain environment-specific measurements. A run passes the basic acceptance gate when the failure rate is 0%, `/predict` has no HTTP 5xx responses, and p95 latency stays within the team-agreed deployment budget. Increase user count only after the baseline passes.

## Evidence status

- E2E test: reproducible locally and in CI.
- Load test: baseline completed against `https://plant-disease-demo.duckdns.org` on 2026-07-12 with a dedicated test account and a real rice-leaf image. The two-minute run ramped to five users and completed 242 requests: 0 failures, including 26 `/api/v1/predict` requests with no HTTP 5xx response. The observed aggregate p95 was 1.5 s; `/api/v1/predict` p95 was 3.2 s. HTML and CSV evidence were generated under `reports/phase6-locust.html` and `reports/phase6-locust_*.csv` (intentionally ignored because they are run-specific artifacts).

The baseline failure-rate and prediction-availability gates passed. No formal team latency budget is documented yet, so the recorded p95 values are an observation rather than an SLA pass/fail verdict.
