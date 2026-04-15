from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from typing import Annotated, TypedDict

import httpx
from fastapi import FastAPI, Query, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# --------------- Pydantic Models ----------------


class Gender(TypedDict):
    name: str
    gender: str | None
    probability: float
    count: int


class GenderResponse(TypedDict):
    name: str
    gender: str
    probability: float
    sample_size: int
    is_confident: bool
    processed_at: str


app = FastAPI()

# --------------------- CORS ---------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_cors_header(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# 3. Custom 422/Validation Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, _exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"status": "error", "message": "Missing or empty name parameter"},
    )


@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, _exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
        },
    )


@app.get("/api/classify")
async def classify(name: Annotated[str, Query(min_length=1)]):
    name = name.strip()
    if not name:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Missing or empty name parameter",
            },
        )

    try:
        async with httpx.AsyncClient() as client:
            api_res = await client.get(
                "https://api.genderize.io/",
                params={"name": name},
                timeout=5.0,
            )
            api_res.raise_for_status()
            data: Gender = api_res.json()
    except httpx.RequestError:
        return JSONResponse(
            status_code=502,
            content={
                "status": "error",
                "message": "Network error",
            },
        )
    except httpx.HTTPStatusError as e:
        return JSONResponse(
            status_code=502,
            content={
                "status": "error",
                "message": f"Bad response from API: {e.response.status_code}",
            },
        )

    if not data["gender"] or data["count"] == 0:
        return JSONResponse(
            status_code=200,
            content={
                "status": "error",
                "message": "No prediction available for the provided name",
            },
        )

    is_confident = data["probability"] >= 0.7 and data["count"] >= 100
    processed_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")

    _data: GenderResponse = {
        "name": data["name"],
        "gender": data["gender"],
        "probability": data["probability"],
        "sample_size": data["count"],
        "is_confident": is_confident,
        "processed_at": processed_at,
    }
    return JSONResponse(status_code=200, content={"status": "success", "data": _data})
