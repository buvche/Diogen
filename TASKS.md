# Task List - Project Diogen

> **Agile Team Structure:** 5 parallel workstreams for efficient development.

---

## 🟢 Agent 1: Backend Developer (API & Core)
**Focus:** FastAPI endpoints, authentication, request handling.

- [x] Implement `core/config.py` (Pydantic Settings)
- [x] Implement `core/logging.py`
- [x] Create `api/main.py` (FastAPI entry point)
- [x] Create `POST /api/ingest/{source}` endpoint
- [x] Add API authentication (`api/auth.py`)
- [x] Add `GET /health` endpoint with DB connectivity check
- [ ] Add OpenAPI documentation customization

---

## 🔵 Agent 2: Data Engineer (Medallion Layers)
**Focus:** Bronze, Silver, Gold data pipeline implementation.

### Bronze Layer
- [x] Create `bronze/models.py` (RawData table with JSONB)
- [ ] Add data validation schema for common sources

### Silver Layer
- [x] Create `silver/models.py` (structured tables)
- [x] Implement `silver/transformers.py` (Polars ETL logic)
- [ ] Create Bronze → Silver scheduled job

### Gold Layer
- [x] Create `gold/models.py` (DORA metrics tables)
- [x] Implement DORA Metrics models:
    - [x] Deployment Frequency
    - [x] Lead Time for Changes
    - [x] Change Failure Rate
    - [x] Mean Time to Recovery

---

## 🟣 Agent 3: Integration Engineer (Connectors)
**Focus:** External API integrations (GitHub, Jira, AWS).

### GitHub Connector
- [x] Implement `connectors/github.py` (REST API client)
- [x] Fetch Pull Requests, Commits, Deployments
- [ ] Implement webhook handler for real-time ingestion

### Jira Connector
- [x] Implement `connectors/jira.py` (REST API client)
- [x] Fetch Issues, Sprints, Changelogs

### AWS Connector (Future)
- [ ] Implement `connectors/aws.py` (CloudWatch, CodePipeline)

---

## 🟠 Agent 4: DevOps Engineer (Infrastructure)
**Focus:** Docker, CI/CD, database migrations.

- [x] Create `docker-compose.yml` (PostgreSQL 15)
- [x] Add `Dockerfile` for the FastAPI application
- [ ] Configure `alembic` for database migrations (Configured, pending initial migration)
- [ ] Create initial migration for Bronze tables
- [x] Add `Makefile` with common commands (Added `tests` alias)
- [ ] Setup GitHub Actions CI/CD pipeline

---

## 🟡 Agent 5: QA & Documentation
**Focus:** Testing, documentation, code quality.

### Testing
- [x] Setup `pytest` with `pytest-asyncio`
- [x] Write test fixtures (`tests/conftest.py`)
- [x] Write integration tests for `/ingest` endpoint (`tests/test_api.py`)
- [ ] Add test fixtures for database mocking

### Documentation
- [x] Update `README.md` with project status
- [x] Create `TASKS.md` with team structure
- [ ] Add API usage examples to README
- [ ] Create `CONTRIBUTING.md`

---

## 📊 Sprint Progress

| Agent | Role | Progress |
|-------|------|----------|
| 🟢 Agent 1 | Backend Developer | █████████░ 90% |
| 🔵 Agent 2 | Data Engineer | ████████░░ 80% |
| 🟣 Agent 3 | Integration Engineer | ███████░░░ 70% |
| 🟠 Agent 4 | DevOps Engineer | ██████░░░░ 60% |
| 🟡 Agent 5 | QA & Documentation | ███████░░░ 70% |

---

## 📁 Files Created This Sprint

```
Diogen/
├── api/
│   ├── main.py          # FastAPI app entry
│   ├── auth.py          # API key authentication
│   └── routes/
│       └── ingest.py    # Ingestion endpoint
├── bronze/
│   └── models.py        # RawData table
├── silver/
│   ├── models.py        # Structured tables
│   └── transformers.py  # ETL logic
├── gold/
│   └── models.py        # DORA metrics
├── connectors/
│   ├── github.py        # GitHub API client
│   └── jira.py          # Jira API client
├── core/
│   ├── config.py        # Settings
│   ├── database.py      # Async DB
│   └── logging.py       # Logging
├── tests/
│   ├── conftest.py      # Fixtures
│   └── test_api.py      # API tests
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── requirements.txt
└── .gitignore
```
