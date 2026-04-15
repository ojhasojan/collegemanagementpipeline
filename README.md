# College Data Pipeline

A production-style data engineering pipeline for college academic data.
Extracts from Google Sheets, loads into PostgreSQL, transforms with dbt,
and orchestrates with Apache Airflow — all running in Docker.

---

## Stack

| Layer         | Tool                        |
|---------------|-----------------------------|
| Package mgr   | uv                          |
| Extract       | Python + gspread + pandas   |
| Load          | psycopg2                    |
| Transform     | dbt (PostgreSQL adapter)    |
| Orchestrate   | Apache Airflow              |
| Database      | PostgreSQL (Docker)         |
| Containers    | Docker + Docker Compose     |
| Logging       | Python logging + pipeline_log table |

---

## Folder Structure

college-pipeline/
├── dags/                  # Airflow DAGs
│   └── college_pipeline_dag.py
├── college_dbt/           # dbt project
│   ├── models/
│   │   ├── staging/       # raw → cleaned
│   │   ├── intermediate/  # business logic
│   │   └── marts/         # final tables
│   ├── seeds/             # reference data (programs, semesters)
│   ├── tests/
│   └── dbt_project.yml
├── extract/               # Python extraction scripts
│   ├── google_sheets.py
│   └── loader.py
├── sql/
│   └── schema.sql
├── docker/
│   └── docker-compose.yml
├── logs/                  # pipeline run logs
├── data/                  # raw CSVs (staging)
├── .env.example
├── pyproject.toml
└── README.md

---

## Setup (Phase 1)

<!-- To be filled as we build -->

## Running the Pipeline

<!-- To be filled as we build -->

## dbt Models

<!-- To be filled as we build -->

## Airflow DAG

<!-- To be filled as we build -->