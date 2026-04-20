from collections.abc import Awaitable, Callable
from typing import Any
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.schemas.schema import (
    AllProfilesParams,
    HNGProfileData,
    ProfileCreate,
    ProfileExistsResponse,
)
from src.app.core.exceptions import ExternalAPIError
from src.app.db.models import UserData
from src.app.db.session import get_db
from src.app.services.profile_service import (
    ProfileService,
    get_profile_service,
)

# from src.clients.genderize.client import

app = FastAPI()

fake_db: list[dict[str, Any]] = []

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


# --------------------- ERROR HANDLING -------------------
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
            "message": "Upstream or server failure",
        },
    )


@app.exception_handler(ExternalAPIError)
async def external_api_exception_handler(_request: Request, exc: ExternalAPIError):
    return JSONResponse(
        status_code=502,
        content={
            "status": "error",
            "message": exc.message,
        },
    )


@app.post("/api/profiles/", status_code=201)
async def create_profile(
    payload: ProfileCreate,
    db: AsyncSession = Depends(get_db),
    profile_service: ProfileService = Depends(get_profile_service),
):
    result = await db.execute(select(UserData).where(UserData.name == payload.name))

    existing_user = result.scalar_one_or_none()

    if existing_user:
        print(f"------{existing_user}--------")
        return ProfileExistsResponse(
            status="success",
            data=HNGProfileData.model_validate(existing_user),
        )

    profile = await profile_service.create_profile(name=payload.name)

    db_user = UserData(**profile.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return HNGProfileData.model_validate(db_user)


@app.get("/api/profiles", status_code=200)
async def get_profiles(
    queries: AllProfilesParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    filters = queries.model_dump(exclude_none=True)

    # python level filtering
    # return [
    #     p for p in fake_db if all(p.get(key) == value for key, value in filters.items())
    # ]

    filters = queries.model_dump(exclude_none=True)

    stmt = select(UserData)

    for key, value in filters.items():
        stmt = stmt.where(getattr(UserData, key) == value)

    result = await db.execute(stmt)
    return result.scalars().all()


@app.get("/api/profiles/{id}", status_code=200)
async def get_profile(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(UserData).where(UserData.id == id),
    )
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Profile not found"},
        )

    return profile


@app.delete("/api/profiles/{id}", status_code=204)
async def delete_profile(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UserData).where(UserData.id == id),
    )
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Profile not found"},
        )

    await db.execute(
        delete(UserData).where(UserData.id == id),
    )

    await db.commit()
