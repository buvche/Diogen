# Diogen
The Easiest, Smartest, Intuitive. DevOps metrics tracker.

# Project DIOGEN 🕯️

> **"Discovering the truth in your engineering data."**

## 🚀 Project Status

| Status | Phase |
|--------|-------|
| ✅ Complete | Phase 1: Foundation & Infrastructure |
| ✅ Complete | Phase 2: Bronze Layer (Raw Ingestion) |
| ✅ Complete | Phase 3: Connectors (GitHub, Jira) |
| ✅ Complete | Phase 4: Silver Layer (ETL Transformers) |
| ✅ Complete | Phase 5: Gold Layer (DORA Metrics) |
| ✅ Complete | Phase 6: API, Auth, CI/CD |
| ⏳ Pending | Phase 7: Scheduler, Dashboard, AWS Connector |

> 📋 See [TASKS.md](TASKS.md) for detailed team assignments and progress.

---

## 👥 Agile Team Structure

| Agent | Role | Responsibility |
|-------|------|----------------|
| 🟢 Agent 1 | **Backend Developer** | API endpoints, authentication, core logic |
| 🔵 Agent 2 | **Data Engineer** | Bronze/Silver/Gold data pipelines |
| 🟣 Agent 3 | **Integration Engineer** | GitHub, Jira, AWS connectors |
| 🟠 Agent 4 | **DevOps Engineer** | Docker, CI/CD, migrations |
| 🟡 Agent 5 | **QA & Documentation** | Testing, docs, code quality |

---

<div align="center">
  <p>
    <a href="#-проект-диоген-македонски">
      <img src="https://img.shields.io/badge/Lang-Македонски-red?style=for-the-badge" alt="Македонски">
    </a>
    &nbsp;&nbsp;&nbsp;
    <a href="#-project-diogen-english">
      <img src="https://img.shields.io/badge/Lang-English-blue?style=for-the-badge" alt="English">
    </a>
  </p>
</div>

---

<a id="mk"></a>
## 🇲🇰 Проект ДИОГЕН (Македонски)

**DIOGEN** е Open Source софтвер за следење на инженерски метрики (DevEx Tracker). Неговата цел е да собира, процесира и визуелизира податоци од различни алатки (Jira, GitHub, AWS) користејќи паметна архитектура за да ја открие "вистината" за перформансите на тимот.

### 🏛️ Архитектура (Medallion Pattern)

Проектот користи адаптација на **Medallion архитектурата** врз PostgreSQL:

1.  **🥉 Bronze Layer (Raw Ingestion):**
    * Директен "dump" на сурови JSON податоци од API сервисите во `JSONB` колони. Без валидација, оптимизирано за брзина на запишување.
2.  **🥈 Silver Layer (Cleaned & Enriched):**
    * Чистење на податоците, дефинирање на типови и екстракција на клучни полиња (Python/Polars -> Structured Tables).
3.  **🥇 Gold Layer (Aggregated Metrics):**
    * Пресметка на бизнис метрики (DORA Metrics, SPACE Framework) спремни за извештаи.

### 🛠️ Технички Стак

* **Јазик:** Python 3.11+
* **Backend:** FastAPI (Async)
* **База на податоци:** PostgreSQL 15+ (Heavy usage of `JSONB`)
* **ORM/Driver:** SQLAlchemy 2.0 + Asyncpg
* **Data Processing:** Polars (High-performance DataFrames)
* **Infrastructure:** Docker & Docker Compose

### 📂 Структура на Проектот

```text
diogen/
├── bronze/         # Скрипти за внес на сурови податоци (Raw Ingestion)
├── silver/         # Трансформации и чистење (Polars логика)
├── gold/           # Агрегации и метрики (SQL Views/KPIs)
├── connectors/     # OpenAPI парсери и генерички клиенти
├── core/           # Конфигурација, Логирање, База (DB Connection)
├── api/            # FastAPI ендпоинти
└── docker-compose.yml
```

---

## 🚀 Quick Start

```bash
# 1. Start PostgreSQL
docker compose up -d

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the API
uvicorn api.main:app --reload


# 4. Test ingestion
curl -X POST http://localhost:8000/api/ingest/github \
  -H "Content-Type: application/json" \
  -d '{"event": "push", "repo": "diogen"}'
```

## 🧪 Testing

Run the automated test suite using the Makefile:

```bash
make tests
```

## ☁️ Deployment

Options:
- **Clever Cloud** — 👉 [Deployment Guide](CLEVER_CLOUD_DEPLOY.md)
- **Golem Network** — Decentralized compute via GVMI images (experimental)

---

## 📜 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
