# Gender Classification API (Stage 0 – HNG Internship)

This is a high-performance FastAPI service that accepts a name, queries the Genderize API, and returns an enriched, structured JSON response.

---

## 🚀 Endpoint

GET /api/classify?name=<your_name>

---

## 📌 Overview

- **Input:** A name string via query parameter
- **Action:** Queries the Genderize API for demographic data
- **Output:** A processed response including confidence flags and timestamps

---

## ⚙️ Processing Rules

Data extracted from the Genderize API:

- `gender`: Predicted gender
- `probability`: Confidence score from the external API
- `count`: Renamed to `sample_size`

Derived logic:

- `is_confident`: `true` only if: probability >= 0.7 AND sample_size >= 100. Otherwise `false`

- `processed_at`: A real-time UTC ISO 8601 timestamp (e.g. `2026-04-11T22:30:00Z`)

---

## 📥 Input Validation

The endpoint strictly enforces input integrity:

- **400 Bad Request:** Returned if `name` is missing, empty, or contains only whitespace
- **422 Unprocessable Entity:** Returned if `name` is not a valid string type

---

## ⚠️ Edge Cases (Genderize API)

If the external API cannot provide a confident prediction (returns `gender: null` or `count: 0`), the service returns:

The service responds:

```json
{
"status": "error",
"message": "No prediction available for the provided name"
}
```

## ✅ Success Response

```json
{
  "status": "success",
  "data": {
    "name": "alicia",
    "gender": "female",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-11T12:00:00Z"
  }
}
```

---

## ❌ Error Response

All errors follow this structure:

```json
{
  "status": "error",
  "message": "<error message>"
}
```
Possible Status Codes: 400, 422, 502 (External API Error), 500.

---

## 🌐 CORS & Infrastructure

- CORS: Enabled for all origins (Access-Control-Allow-Origin: *).

- Performance: - Utilizes connection pooling (shared httpx.AsyncClient) to stay well under the 500ms response time limit.

- Asynchronous request handling to support high concurrency.

---

## 🧠 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com)
- [httpx](https://www.python-httpx.org) — async HTTP client
- Python 3.12+
- [Genderize API](https://genderize.io)

---

## ⚡ Performance

- Fully async request handling
- Response time under 500ms (excluding external API latency)
- Safe for concurrent requests

---

## ▶️ Running Locally

```bash
poetry install
uvicorn main:app --reload
```

---

## 📡 Example Request
http://localhost:8000/api/classify?name=alicia

---

## 🧩 Author

Built by Teslim Balogun as part of the **HNGi14 Internship — Stage 0 Task in 2026**.