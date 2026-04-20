# 📊 HNG Stage 1 -- Profile Aggregation API

A FastAPI-based service that aggregates user demographic data from
external APIs, applies classification logic, stores results in a
PostgreSQL database, and exposes REST endpoints for managing profiles.

------------------------------------------------------------------------

## 🚀 Overview

This service:

-   Accepts a user name\
-   Fetches data from 3 external APIs:
    -   Genderize\
    -   Agify\
    -   Nationalize\
-   Applies classification rules (age group + top nationality)\
-   Stores processed profiles in a database\
-   Prevents duplicate profile creation\
-   Serves stored profiles via REST API

------------------------------------------------------------------------

## 🌐 External APIs Used

-   https://api.genderize.io?name={name}\
-   https://api.agify.io?name={name}\
-   https://api.nationalize.io?name={name}

All APIs are free and require no authentication.

------------------------------------------------------------------------

## 🧠 Business Logic

### 👤 Age Group Classification

-   0--12 → child\
-   13--19 → teenager\
-   20--59 → adult\
-   60+ → senior

### 🌍 Nationality Selection

-   Select country with the highest probability from Nationalize API

------------------------------------------------------------------------

## 📡 API Endpoints

### Create Profile

POST /api/profiles

Request: { "name": "ella" }

Response: { "status": "success", "data": { "id": "uuid-v7", "name":
"ella", "gender": "female", "gender_probability": 0.99, "sample_size":
1234, "age": 46, "age_group": "adult", "country_id": "NG",
"country_probability": 0.85, "created_at": "2026-04-01T12:00:00Z" } }

------------------------------------------------------------------------

## ⚠️ Error Handling

{ "status": "error", "message": "error message" }

------------------------------------------------------------------------

## 🧱 Data Rules

-   UUID v7 for IDs\
-   ISO 8601 UTC timestamps

------------------------------------------------------------------------

## 🗄️ Database

PostgreSQL with SQLAlchemy ORM.

------------------------------------------------------------------------

## ⚙️ Running the Project

pip install
alembic upgrade head; uvicorn src.app.main:app --reload
