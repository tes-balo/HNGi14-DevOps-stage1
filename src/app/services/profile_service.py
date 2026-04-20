from typing import Any
from uuid import UUID

from fastapi import Depends, HTTPException, status

from src.app.common.schemas.schema import HNGProfileCreateData
from src.app.services.aggregation_service import (
    AggregationService,
    get_aggregation_service,
)


class ProfileService:
    """Handles creation of complete user profiles from aggregated data."""

    def __init__(
        self,
        aggregation_service: AggregationService,
    ):
        self.aggregation_service = aggregation_service

    async def create_profile(self, name: str):
        """Create a full profile for a given name.

        This method orchestrates:
        - data aggregation from external services
        - selection of most probable country
        - generation of metadata (id, timestamp)
        - formatting into API response schema
        """
        data = await self.aggregation_service.aggregate(name)
        top_country = max(data.countries, key=lambda c: c.probability)
        print("TOP COUNTRY:", top_country.country)
        print("TOP PROBABILITY:", top_country.probability)
        # compute metadata
        # profile_id = generate_id()
        # created_at = utc_now_iso()

        return HNGProfileCreateData(
            name=name,
            gender=data.gender.gender,
            gender_probability=data.gender.gender_probability,
            sample_size=data.gender.sample_size,
            age=data.age.age,
            age_group=data.age.age_group,
            country_id=top_country.country,
            country_probability=top_country.probability,
        )


def get_profile_service(
    aggregation_service: AggregationService = Depends(get_aggregation_service),
) -> ProfileService:
    return ProfileService(aggregation_service)


def get_profile(id: str, db: list[dict[str, Any]]):
    for record in db:
        if record["id"] == id:
            return record

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "status": "error",
            "message": "Profile not found",
        },
    )


def get_all_profiles(params: dict[str, str], db: list[dict[str, Any]]):
    return db


def profile_exists(id: UUID, db: list[dict[str, Any]]):
    return any(record["id"] == id for record in db)


def get_profile_by_name(name: str, db: list[dict[str, Any]]):
    for record in db:
        if record["name"] == name:
            return record
    return None
