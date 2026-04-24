from typing import Any

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.schemas.schema import (
    OrderEnum,
    SeedData,
    SortEnum,
)
from src.app.db.base_model import BaseModel
from src.app.db.models import UserData

PROFILE_SORT_FIELDS = {
    "age": UserData.age,
    "created_at": UserData.created_at,
    "gender_probability": UserData.gender_probability,
}


# SQLAlchemyModelType = TypeVar("SQLAlchemyModelType", bound=BaseModel)
class BaseRepository[T: BaseModel]:
    def __init__(self, db: AsyncSession, model: type[T]):
        self.db = db
        self.model = model

    async def find_by_id(self, record_id: str) -> T | None:
        result = await self.db.execute(
            select(self.model).where(self.model.id == record_id),
        )
        return result.scalar_one_or_none()

    async def delete(self, record_id: str) -> T | None:
        obj = await self.find_by_id(record_id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()


class UserRepository(BaseRepository[BaseModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, UserData)

    # only add user-specific methods here
    async def find_by_name(self, name: str):
        result = await self.db.execute(select(UserData).where(UserData.name == name))
        return result.scalar_one_or_none()

    # -------------- database seed  create funPzshction (to be called in seed script) ---------------
    async def create_users_from_json(self, data: SeedData) -> None:
        if not data or not isinstance(data, dict):  # type: ignore
            return
        stmt = insert(UserData).values(
            name=data["name"],
            gender=data["gender"],
            gender_probability=data["gender_probability"],
            age=data["age"],
            age_group=data["age_group"],
            country_id=data["country_id"],
            country_name=data["country_name"],
            country_probability=data["country_probability"],
        )

        stmt = stmt.on_conflict_do_nothing(
            constraint="uq_user_profile_name",  # because name is UNIQUE
        )

        await self.db.execute(stmt)

    async def get_all_profiles(
        self,
        filters: dict[str, Any],
        sort_by: SortEnum | None,
        order: OrderEnum,
        page: int,
        limit: int,
    ):
        """Retrieve profiles from the database with filtering, sorting, and pagination.

        Args:
        filters (dict[str, Any]): Dictionary of filter conditions.
        sort_by (SortEnum | None): Field to sort by.
        order (OrderEnum): Sorting direction (asc/desc).
        page (int): Page number.
        limit (int): Number of records per page.

        Returns:
        list[UserData]: List of matching profiles.

        """
        base_stmt = select(UserData)
        stmt = base_stmt

        # ---------------- filters ----------------
        if "gender" in filters:
            # stmt = stmt.where(UserData.gender == filters["gender"])
            gender = filters["gender"]

            if isinstance(gender, list):
                stmt = stmt.where(UserData.gender.in_(gender))  # type: ignore
            else:
                stmt = stmt.where(UserData.gender == gender)

        if "age_group" in filters:
            stmt = stmt.where(UserData.age_group == filters["age_group"])

        if "country_id" in filters:
            stmt = stmt.where(UserData.country_id == filters["country_id"])

        if "min_age" in filters:
            stmt = stmt.where(UserData.age >= filters["min_age"])

        if "max_age" in filters:
            stmt = stmt.where(UserData.age <= filters["max_age"])

        # ---------------- total count ----------------
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar_one()

        # ---------------- sorting ----------------

        if sort_by:
            column = PROFILE_SORT_FIELDS.get(sort_by.value)
            if not column:
                raise ValueError("Invalid sort field")

            stmt = stmt.order_by(
                column.desc() if order == OrderEnum.desc else column.asc(),
            )

        # ---------------- pagination ----------------
        offset = (page - 1) * limit
        stmt = stmt.limit(limit).offset(offset)

        result = await self.db.execute(stmt)
        data = result.scalars().all()
        for d in data:
            if d.age_group:
                d.age_group = d.age_group.lower()

        return data, total
        # for key in filters:
        #     if filters[key]:
        #         query = query.


# need to handle sort_by seperately
