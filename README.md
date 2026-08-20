# AI-Powered Data Analytics Platform

[![CI](https://github.com/example/ai-analytics-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/example/ai-analytics-platform/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![scikit--learn](https://img.shields.io/badge/scikit--learn-1.5%2B-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-oriented foundation for an AI-powered analytics product. The first part combines a typed FastAPI service with reusable data-processing and machine-learning components for anomaly detection, supervised prediction, and text sentiment analysis.

The project is designed to demonstrate senior-level engineering practices: explicit boundaries between HTTP, domain services, and models; validated request and response contracts; deterministic preprocessing; structured logging; testable dependency-free components; and reproducible local execution through Docker and CI.

## Architecture overview

```text
┌──────────────────────┐       JSON/HTTP       ┌────────────────────────┐
│ Analytics consumers  │ ────────────────────▶ │ FastAPI application     │
│ dashboards / clients  │ ◀──────────────────── │ routers + validation    │
└──────────────────────┘                       └───────────┬────────────┘
                                                           │
                         ┌─────────────────────────────────┼────────────────────────┐
                         │                                 │                        │
                 ┌───────▼────────┐                ┌───────▼────────┐       ┌───────▼────────┐
                 │ Data processing │                │ ML inference    │       │ NLP sentiment   │
                 │ cleaning + stats│                │ train/predict   │       │ lexicon scoring │
                 └───────┬────────┘                └───────┬────────┘       └────────────────┘
                         │                                 │
                 ┌───────▼─────────────────────────────────▼───────┐
                 │ Reusable schemas, preprocessing, logging, config │
                 └───────────────────────────────────────────────────┘

┌──────────────────────────────┐       artifacts       ┌───────────────────────┐
│ ml-module                    │ ────────────────────▶ │ python-backend/models │
│ EDA, preprocessing, training │                       │ loaded model wrappers │
│ and evaluation               │                       └───────────────────────┘
└──────────────────────────────┘
```

## Technology stack

| Area | Technology | Purpose |
|---|---|---|
| API | FastAPI, Uvicorn | Async-ready REST API and OpenAPI documentation |
| Validation | Pydantic v2, pydantic-settings | Typed contracts and environment configuration |
| Analytics | pandas, NumPy, SciPy | Tabular processing and descriptive statistics |
| Machine learning | scikit-learn, joblib | Robust preprocessing, anomaly detection, and regression |
| NLP | Python service with transparent lexicon scoring | Explainable sentiment analysis without an external runtime dependency |
| Testing | pytest, HTTPX | Unit and API-level verification |
| Operations | Docker Compose, GitHub Actions | Repeatable local development and continuous integration |

## Features in this first part

The API exposes a health endpoint, descriptive analytics for tabular records, an anomaly-detection endpoint based on Isolation Forest, a supervised prediction endpoint backed by a persisted scikit-learn pipeline, and sentiment analysis for batches of text. Input validation rejects malformed or unsafe payloads before business logic is invoked, while service-level exceptions are converted into consistent HTTP responses.

The ML module includes a reusable preprocessing pipeline, a synthetic-data-friendly training script, an evaluation script with regression and classification metrics, and an exploratory-analysis script that can be run as a notebook-style Python file. The scripts are intentionally CLI-oriented so they can later be scheduled or integrated into a model registry.

## Repository layout

```text
.
├── python-backend/        # FastAPI service, domain services, model wrappers, and tests
├── ml-module/             # EDA, preprocessing, training, and evaluation workflows
├── .github/workflows/     # CI pipeline
├── docker-compose.yml     # Local service orchestration
├── .env.example           # Documented environment variables
└── README.md
```

## Quick start

### Local Python setup

Python 3.11 or newer is recommended. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r python-backend/requirements.txt
pip install -r ml-module/requirements.txt
uvicorn app.main:app --app-dir python-backend --reload
```

The interactive API documentation is available at `http://localhost:8000/docs`; the health check is available at `http://localhost:8000/api/v1/health`.

### Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

The container runs the API with a production-style Uvicorn command and mounts the model artifact directory for local iteration. Environment variables are read from `.env` and can be overridden by the shell.

### Train a model

```bash
python ml-module/models/train_model.py \
  --output-dir python-backend/artifacts \
  --n-samples 1200 \
  --random-state 42
```

The generated artifact can then be used by the prediction endpoint by setting `MODEL_ARTIFACT_PATH` to the resulting `.joblib` file.

## API examples

Analyze numeric and categorical records:

```bash
curl -X POST http://localhost:8000/api/v1/analysis/summary \
  -H 'Content-Type: application/json' \
  -d '{"records":[{"revenue":120.5,"region":"west"},{"revenue":98.2,"region":"east"}]}'
```

Score sentiment:

```bash
curl -X POST http://localhost:8000/api/v1/analysis/sentiment \
  -H 'Content-Type: application/json' \
  -d '{"texts":["The onboarding experience was excellent.","Support was slow and frustrating."]}'
```

Detect anomalies in feature vectors:

```bash
curl -X POST http://localhost:8000/api/v1/predictions/anomalies \
  -H 'Content-Type: application/json' \
  -d '{"records":[{"latency_ms":20,"errors":0},{"latency_ms":900,"errors":40}],"contamination":0.1}'
```

## Configuration

All settings are environment-driven and have safe local defaults. Production deployments should set a strong `API_KEY`, restrict `CORS_ORIGINS`, provide an externally managed model artifact, and set `ENVIRONMENT=production`. The current API-key middleware is optional by default so local exploration remains frictionless.

## Quality and engineering standards

The project uses type hints throughout application code, structured logs with request correlation IDs, explicit service exceptions, deterministic random seeds in ML workflows, and tests that target both pure business logic and HTTP contracts. CI runs formatting/lint checks, static compilation, unit tests, and a smoke import of both packages.

## Roadmap

Future parts can add a persistent data store, asynchronous ingestion, a model registry, feature-importance explanations, dashboard UI, role-based authentication, streaming metrics, and scheduled retraining. The current boundaries are intentionally suitable for those extensions without coupling the API layer to a specific storage or frontend implementation.

## License

This project is released under the [MIT License](LICENSE).

## References

[1]: https://fastapi.tiangolo.com/ "FastAPI documentation"
[2]: https://scikit-learn.org/stable/ "scikit-learn documentation"
[3]: https://docs.pydantic.dev/latest/ "Pydantic documentation"
[4]: https://docs.docker.com/compose/ "Docker Compose documentation"

## Java backend

The `java-backend/` module is a Spring Boot 3 REST service that acts as the secure orchestration layer for the platform. It demonstrates a conventional enterprise architecture with controllers, services, immutable domain models, repositories, DTO validation, centralized exception handling, and environment-driven configuration. JWT authentication is stateless and the sample repository is intentionally in-memory so the module runs without an external database; the repository boundary is ready for a JPA or document-store adapter.

Pipeline execution demonstrates three maintainable design patterns. `PipelineTaskFactory` resolves a named workload, `ProcessingStrategy` implementations encapsulate algorithm-specific behavior, and `PipelineEventListener` observes lifecycle events for logging or future event-bus integration. The Java layer is designed to delegate intensive ML inference to the existing Python service rather than duplicate the model runtime.

Run it locally from the repository root:

```bash
cd java-backend
mvn spring-boot:run
```

The service listens on `http://localhost:8081/api`. A seeded development user is available as `demo@analytics.dev` with password `demo-password`; set `JWT_SECRET` to a strong value before any deployment. Build the container with `docker build -t analytics-platform-api java-backend`.

## Frontend

The `frontend/` module is a dependency-light static client with a polished marketing landing page and an analytics dashboard. It uses semantic HTML, CSS custom properties, responsive grid/flex layouts, accessible controls, a persisted dark/light theme, and Chart.js for the revenue performance visualization. `js/api.js` provides a small authenticated fetch client for the Java orchestration API, while the dashboard remains usable in demo mode when the API is not running.

Serve the frontend locally with any static server, for example:

```bash
python -m http.server 5500 --directory frontend
```

Open `http://localhost:5500/index.html` for the product page or `http://localhost:5500/dashboard.html` for the command center. The default API URL is `http://localhost:8081/api`; override it before loading the page with `window.SIGNALFORGE_API` when deploying behind a different gateway.

## Extended repository layout

```text
.
├── python-backend/        # Part 1: FastAPI service and ML-facing API
├── ml-module/             # Part 1: preprocessing, training, evaluation, and EDA
├── java-backend/          # Part 2: Spring Boot JWT orchestration API
├── frontend/              # Part 2: responsive landing page and dashboard
├── .github/workflows/     # CI pipeline
└── README.md
```

The two backend modules intentionally have separate responsibilities: Python owns data science and model execution, while Java owns authenticated workflow orchestration and integration contracts. This separation provides a credible path to independently scaling compute-heavy inference and business-facing API traffic.

