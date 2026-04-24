from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.app.common.schemas.schema import (
    PaginationParams,
    ProfileFilters,
    SortParams,
)
from src.app.common.utils.query_parser import parse_query
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
        status_code=422,
        content={
            "status": "error",
            "message": "Invalid query parameters",
        },
    )


@app.exception_handler(RequestValidationError)
async def bad_request_handler(_request: Request, _exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"status": "error", "message": "Missing or empty parameter"},
    )


@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, _exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Server failure",
        },
    )


@app.exception_handler(Exception)
async def not_found_exception_handler(_request: Request, _exc: Exception):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": "Profile not found",
        },
    )


# # @app.exception_handler(Exception)
# async def exception_handler(_request: Request, exc: HTTPException):
#     return JSONResponse(
#         status_code=404,
#         content={
#             "status": "error",
#             "message": "Profile not found",
#         },
#     )


# @app.post("/api/profiles/", status_code=201)
# async def create_profile(
#     payload: ProfileCreate,
#     db: AsyncSession = Depends(get_db),
#     profile_service: ProfileService = Depends(get_profile_service),
# ):
#     result = await db.execute(select(UserData).where(UserData.name == payload.name))

#     existing_user = result.scalar_one_or_none()

#     if existing_user:
#         print(f"------{existing_user}--------")
#         return ProfileExistsResponse(
#             status="success",
#             data=HNGProfileData.model_validate(existing_user),
#         )

#     profile = await profile_service.create_profile(name=payload.name)

#     db_user = UserData(**profile.model_dump())
#     db.add(db_user)
#     await db.commit()
#     await db.refresh(db_user)

#     return HNGProfileData.model_validate(db_user)


@app.get("/api/profiles")
async def get_profiles(
    filters: ProfileFilters = Depends(),
    sort: SortParams = Depends(),
    pagination: PaginationParams = Depends(),
    profile_service: ProfileService = Depends(get_profile_service),
):
    """Retrieve user profiles using structured query parameters.

    Supports:
    - Filtering (gender, age, country, etc.)
    - Sorting (by selected fields)
    - Pagination (page and limit)

    Returns:
        list[HNGProfileData]: List of matching profiles.

    """
    return await profile_service.get_profiles(
        filters=filters,
        sort=sort,
        pagination=pagination,
    )


@app.get("/api/profiles/search", summary="Search profiles using natural language")
async def search_profiles(
    q: str = Query(...),
    sort: SortParams = Depends(),
    pagination: PaginationParams = Depends(),
    profile_service: ProfileService = Depends(get_profile_service),
):
    """Search profiles using natural language queries.

    Converts plain English queries into structured filters.

    Examples:
        - "young males from nigeria"
        - "females above 30"
        - "adult males from kenya"

    Args:
        q (str): Natural language query string.

    Returns:
        list[HNGProfileData]: List of matching profiles.

    """
    parsed = parse_query(query=q)
    if not parsed.filters:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": "Unable to interpret query",
            },
        )
    return await profile_service.search_profiles(
        raw_query=q,
        pagination=pagination,
        sort=sort,
    )


# @app.get("/api/profiles/{id}", status_code=200)
# async def get_profile(id: UUID, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(
#         select(UserData).where(UserData.id == id),
#     )
#     profile = result.scalar_one_or_none()

#     if not profile:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail={"status": "error", "message": "Profile not found"},
#         )

#     return profile


# @app.delete("/api/profiles/{id}", status_code=204)
# async def delete_profile(
#     id: UUID,
#     db: AsyncSession = Depends(get_db),
# ):
#     result = await db.execute(
#         select(UserData).where(UserData.id == id),
#     )
#     profile = result.scalar_one_or_none()

#     if not profile:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail={"status": "error", "message": "Profile not found"},
#         )

#     await db.execute(
#         delete(UserData).where(UserData.id == id),
#     )

#     await db.commit()
