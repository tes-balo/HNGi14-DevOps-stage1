from src.app.common.schemas.schema import (
    PaginationParams,
    ProfileFilters,
    SortParams,
)
from src.app.repos.repos import UserRepository


class UserService:
    """Service layer for user-related operations."""

    def __init__(self, user_repo: UserRepository):
        """Initialize service with repository.

        Args:
            user_repo (UserRepository): Repository instance.

        """
        self.user_repo = user_repo

    async def get_user(self, user_id: str):
        """Retrieve a single user by ID.

        Args:
            user_id (str): Unique identifier of the user.

        Returns:
            UserData: The user record.

        Raises:
            Exception: If user is not found.

        """
        user = await self.user_repo.find_by_id(user_id)
        if not user:
            raise Exception("User not found")
        return user

    async def get_all_profiles(
        self,
        filters: ProfileFilters,
        sort: SortParams,
        pagination: PaginationParams,
    ):
        """Retrieve all profiles using structured query inputs.

        Args:
            filters (ProfileFilters): Filtering conditions.
            sort (SortParams): Sorting configuration.
            pagination (PaginationParams): Pagination settings.

        Returns:
            list[UserData]: List of profiles.

        """
        filter_dict = filters.model_dump(exclude_none=True)

        return await self.user_repo.get_all_profiles(
            filters=filter_dict,
            sort_by=sort.sort_by,
            order=sort.order,
            page=pagination.page,
            limit=pagination.limit,
        )
