from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.schemas.schema import (
    HNGProfileData,
    PaginatedResponse,
    PaginationParams,
    ProfileFilters,
    SortParams,
)
from src.app.common.utils.query_parser import parse_query
from src.app.db.session import get_db
from src.app.repos.repos import UserRepository


class ProfileService:
    """Service layer responsible for orchestrating profile retrieval logic.

    Handles:
    - Structured filtering (from API query params)
    - Natural language search parsing
    - Pagination and sorting delegation to repository
    """

    def __init__(self, repo: UserRepository):
        """Initialize the service with a user repository.

        Args:
            repo (UserRepository): Repository for database operations.

        """
        self.repo = repo

    async def get_profiles(
        self,
        filters: ProfileFilters,
        sort: SortParams,
        pagination: PaginationParams,
    ):
        """Retrieve profiles using structured query parameters.

        Args:
            filters (ProfileFilters): Filtering conditions (gender, age, country, etc.).
            sort (SortParams): Sorting configuration.
            pagination (PaginationParams): Pagination settings.

        Returns:
            list[UserData]: List of matching profiles.

        """
        raw_filters = filters.model_dump(exclude_none=True)

        clean_filters = {}

        for k, v in raw_filters.items():
            if v is None:
                continue

            # convert enums → strings
            if isinstance(v, list):
                clean_filters[k] = [
                    x.value if hasattr(x, "value") else str(x) for x in v
                ]
            else:
                clean_filters[k] = v.value if hasattr(v, "value") else v
        data, total = await self.repo.get_all_profiles(
            filters=clean_filters,
            sort_by=sort.sort_by,
            order=sort.order,
            page=pagination.page,
            limit=pagination.limit,
        )

        return PaginatedResponse[HNGProfileData](
            page=pagination.page,
            limit=pagination.limit,
            total=total,
            data=[HNGProfileData.model_validate(d) for d in data],
        )

    async def search_profiles(
        self,
        raw_query: str,
        pagination: PaginationParams,
        sort: SortParams,
    ):
        """Perform natural language search on profiles.

        Converts plain English query into structured filters,
        then delegates to repository for execution.

        Args:
            raw_query (str): Natural language query (e.g. "young males from nigeria").
            pagination (PaginationParams): Pagination settings.
            sort (SortParams): Sorting configuration.

        Returns:
            list[UserData]: List of matching profiles.

        """
        parsed = parse_query(query=raw_query, page=pagination.page)
        if not parsed.filters:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "message": "Unable to interpret query",
                },
            )

        data, total = await self.repo.get_all_profiles(
            filters=parsed.filters,
            sort_by=sort.sort_by,
            order=sort.order,
            page=pagination.page,
            limit=pagination.limit,
        )

        return PaginatedResponse[HNGProfileData](
            page=pagination.page,
            limit=pagination.limit,
            total=total,
            data=[HNGProfileData.model_validate(d) for d in data],
        )

        # return await self.repo.get_all_profiles(
        #     filters=parsed.filters,
        #     sort_by=sort.sort_by,
        #     order=sort.order,
        #     page=pagination.page,
        #     limit=pagination.limit,
        # )


def get_profile_service(
    db: AsyncSession = Depends(get_db),
) -> ProfileService:
    """Dependency injector for ProfileService.

    Creates a repository instance using the database session
    and injects it into the service.

    Args:
        db (AsyncSession): Database session.

    Returns:
        ProfileService: Initialized service instance.

    """
    repo = UserRepository(db)
    return ProfileService(repo)
