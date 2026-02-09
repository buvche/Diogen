# Diogen
The Easiaest, Smartest, Intuitive. Devops metrics tracker.

# Project DIOGEN 🕯️

> **"Discovering the truth in your engineering data."**

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
