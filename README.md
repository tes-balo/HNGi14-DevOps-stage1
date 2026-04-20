📊 HNG Stage 1 – Profile Aggregation API

A FastAPI-based service that aggregates user demographic data from external APIs, applies classification logic, stores results in a PostgreSQL database, and exposes REST endpoints for managing profiles.

🚀 Overview

This service:

Accepts a user name
Fetches data from 3 external APIs:
Genderize
Agify
Nationalize
Applies classification rules (age group + top nationality)
Stores processed profiles in a database
Prevents duplicate profile creation
Serves stored profiles via REST API
🌐 External APIs Used
https://api.genderize.io?name={name}
https://api.agify.io?name={name}
https://api.nationalize.io?name={name}

All APIs are free and require no authentication.

🧠 Business Logic
👤 Age Group Classification

Based on Agify age prediction:

0–12 → child
13–19 → teenager
20–59 → adult
60+ → senior
🌍 Nationality Selection

From Nationalize API response:

Select country with highest probability
📡 API Endpoints
1. Create Profile
POST /api/profiles
Request
{
  "name": "ella"
}
Success Response (201)
{
  "status": "success",
  "data": {
    "id": "uuid-v7",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 46,
    "age_group": "adult",
    "country_id": "NG",
    "country_probability": 0.85,
    "created_at": "2026-04-01T12:00:00Z"
  }
}
Duplicate Handling

If profile already exists:

{
  "status": "success",
  "message": "Profile already exists",
  "data": { ...existing profile }
}
2. Get Single Profile
GET /api/profiles/{id}
Response
{
  "status": "success",
  "data": {
    "id": "uuid",
    "name": "emmanuel",
    "gender": "male",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 25,
    "age_group": "adult",
    "country_id": "NG",
    "country_probability": 0.85,
    "created_at": "2026-04-01T12:00:00Z"
  }
}
3. Get All Profiles
GET /api/profiles
Optional Query Params (case-insensitive)
gender
country_id
age_group

Example:

/api/profiles?gender=male&country_id=NG
Response
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": "id-1",
      "name": "emmanuel",
      "gender": "male",
      "age": 25,
      "age_group": "adult",
      "country_id": "NG"
    }
  ]
}
4. Delete Profile
DELETE /api/profiles/{id}
Response
204 No Content
⚠️ Error Handling

All errors follow:

{
  "status": "error",
  "message": "error message"
}
Client Errors
400 → Missing or empty name
422 → Invalid request type
404 → Profile not found
External API Failures (CRITICAL)

If any API fails:

Genderize
Agify
Nationalize

Return:

{
  "status": "error",
  "message": "Genderize returned an invalid response"
}

(or Agify / Nationalize accordingly)

Edge Cases
Gender = null OR count = 0 → return 502
Age = null → return 502
No country data → return 502
Do NOT store invalid external responses
🧱 Data Rules
IDs → UUID v7
Timestamps → ISO 8601 UTC

Example:

2026-04-01T12:00:00Z
🗄️ Database

Profiles are persisted in PostgreSQL using SQLAlchemy ORM.

Key fields:

name
gender
age
age_group
country_id
probabilities
created_at

Duplicate prevention is enforced on name.

🌍 CORS

Required header:

Access-Control-Allow-Origin: *

Without this, automated graders cannot access the API.

🏗️ Tech Stack
FastAPI
SQLAlchemy (async)
PostgreSQL
Pydantic v2
Uvicorn
🧪 Design Highlights
Clean service-based architecture
External API aggregation layer
Strong separation of concerns
Deduplication logic at service level
Enum-based classification system
Fully async request handling
⚙️ Running the Project
poetry install
poetry run uvicorn src.app.main:app --reload
📌 Notes
All external APIs are called asynchronously
Aggregation is done before persistence
Profile creation is idempotent (name-based)
System is designed for deterministic responses