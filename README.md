Student Academic Analytics Platform
Data Engineering Project

Introduction
This repository documents the design and implementation of a student academic analytics platform built using modern data engineering practices.
The project focuses on data modeling, transformation, governance, and secure access rather than frontend application development.
The platform supports analytical use cases such as:

student‑level academic performance analysis
subject‑wise and exam‑wise insights
attendance and enrollment analytics
identity‑aware, secure access to analytical data


Technology Stack
Data & Analytics

PostgreSQL – primary relational and analytical database
Supabase – managed PostgreSQL with authentication and security features
dbt (Data Build Tool) – SQL‑based transformations and analytics modeling
SQL – data transformation, aggregation, and analysis
Python – data ingestion, preprocessing, and orchestration

DevOps & Tooling

Docker – containerization of data environments
GitHub – version control and documentation


Architecture Overview
The project follows a layered analytics architecture aligned with industry standards and analytical best practices.
Source Tables
     ↓
Bronze Models
     ↓
Silver Models
     ↓
Gold Analytics (Fact & Dimension Tables)
     ↓
Secure Analytics Access (RLS)


Operational Data Layer
The operational layer consists of normalized tables designed for ingestion and transactional integrity.
Key entities include:

students
subjects
teachers
programs
enrollments
marks
attendance

These tables are optimized for data capture, not analytics.

Analytics Modeling with dbt
All transformations are implemented using dbt, enabling reproducible, version‑controlled analytics pipelines.
Bronze Layer

source‑aligned raw tables
schema normalization and type casting
minimal transformation

Purpose: ensure traceability and ingestion reliability.

Silver Layer

standardized naming conventions
data cleaning and deduplication
referential integrity enforcement

Purpose: produce trusted intermediate datasets.

Gold Layer
The Gold layer contains analytics‑ready models built using star schema design.
Fact Tables

fact_marks
fact_attendance
fact_enrollments

Fact tables:

have clearly defined grain
store measurable metrics
reference dimension identifiers

Dimension Tables

dim_student
dim_subject
dim_teacher

Dimensions provide descriptive context for analytics.

Star Schema Design
The analytical schema follows a star schema pattern to support performance and simplicity.
Typical relationships:

dim_student → fact_marks
dim_subject → fact_marks
dim_teacher → fact_enrollments

This design enables efficient aggregation and BI‑compatible analysis.

Data Transformations
Transformations implemented in dbt include:

joining normalized source tables
metric calculations for marks and attendance
key normalization and integrity checks
materialization as tables and views

dbt provides:

modular SQL models
transformation lineage
reproducible runs
version control via GitHub


Data Quality and Validation
The project incorporates foundational data quality concepts:

primary key enforcement
non‑null constraints
consistent data grain
referential integrity validation

These practices contribute to data reliability and trustworthiness.

Security and Access Control
Authentication Context
Supabase authentication is used to manage user identities.
Each authenticated user is represented by a unique identifier stored in auth.users.

Row Level Security (RLS)
Data access is governed using Row Level Security directly in PostgreSQL.
Key design aspects:

user‑to‑entity mapping tables
identity‑aware SQL conditions
centralized enforcement at the database layer

Security is independent of any frontend logic and follows the principle of least privilege.

Python Usage
Python is used to support the data pipeline for:

loading source data
preprocessing and validation
preparing datasets for dbt transformation
orchestration and execution support

This reflects the standard data engineering pattern:

Python for orchestration
SQL/dbt for transformation and analytics


Containerization with Docker
Docker is used to ensure environment consistency and reproducibility.
Use cases include:

containerized PostgreSQL development environments
reproducible dbt execution contexts
dependency isolation across systems

This approach simplifies onboarding and supports portable analytics workflows.

Version Control with GitHub
GitHub is used for:

managing dbt models and SQL transformations
tracking schema and pipeline changes
maintaining project documentation
ensuring reproducibility and transparency

The repository represents the full lifecycle of the data platform.

Project Scope
This project intentionally excludes:

frontend frameworks
browser‑side authentication logic
UI and application state management

The scope is strictly aligned with data engineering responsibilities rather than application development.

Skills Demonstrated
This project demonstrates practical experience in:

data modeling and star schema design
SQL analytics and transformations
dbt‑based ELT workflows
PostgreSQL governance and security
Row Level Security (RLS)
containerized data environments
version‑controlled analytics pipelines