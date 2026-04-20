import asyncio

from fastapi import Depends

from src.app.common.schemas.schema import ProfileAggregateResponse
from src.app.services.age_service import AgeService, get_age_service
from src.app.services.gender_service import GenderService, get_gender_service
from src.app.services.nation_service import NationService, get_nation_service


class AggregationService:
    """Coordinate multiple external services to build a unified user profile.

    This service concurrently fetches gender, age, and nationality predictions,
    then combines them into a single structured response.

    It acts purely as an orchestration layer and does not contain business
    decision logic (e.g., selecting the top country).
    """

    def __init__(
        self,
        gender_service: GenderService,
        age_service: AgeService,
        nation_service: NationService,
    ):
        """Initialize dependencies for aggregation service."""
        self.gender_service = gender_service
        self.age_service = age_service
        self.nation_service = nation_service

    async def aggregate(self, name: str) -> ProfileAggregateResponse:
        """Aggregate profile information for a given name using multiple external services.

        This method concurrently fetches gender, age, and nationality predictions,
        then combines the results into a single response object.

        The external calls are executed in parallel using asyncio.gather for efficiency.

        Args:
            name (str): The name to analyze across all services.

        Returns:
            ProfileAggregateResponse: A unified profile containing:
                - Gender prediction
                - Age prediction
                - List of nationality probabilities

        Notes:
            - All external API calls are executed concurrently for performance.
            - The aggregation layer does not perform business decision logic (e.g., selecting top country)
            - It returns full data.

        """
        # run all requests concurrently 🔥
        gender_task = self.gender_service.process_gender(name)
        age_task = self.age_service.process_age(name)
        nation_task = self.nation_service.process_nation(name)

        gender, age, nation = await asyncio.gather(
            gender_task,
            age_task,
            nation_task,
        )
        print("RAW NATION RESPONSE:", nation)

        return ProfileAggregateResponse(
            name=name,
            gender=gender,
            age=age,
            countries=nation,
        )


def get_aggregation_service(
    gender_service: GenderService = Depends(get_gender_service),
    age_service: AgeService = Depends(get_age_service),
    nation_service: NationService = Depends(get_nation_service),
) -> AggregationService:
    """Provide an instance of AggregationService with its dependencies.

    This function is used by FastAPI's dependency injection system to construct
    an AggregationService with the required underlying services.

    Each dependency (gender, age, nation) is resolved automatically by FastAPI,
    allowing the aggregation layer to remain decoupled from instantiation logic.

    Args:
        gender_service (GenderService): Service for gender prediction.
        age_service (AgeService): Service for age prediction.
        nation_service (NationService): Service for nationality prediction.

    Returns:
        AggregationService: A fully initialized aggregation service instance.

    """
    return AggregationService(gender_service, age_service, nation_service)


# aggregation_service = AggregationService()

# FIX: ------------------- MAKE SERVICE STATELESS AND PURELY FUNCTIONAL-----------

# def build_profile(name, gender, age, nation) -> ProfileAggregateResponse:
#     return ProfileAggregateResponse(
#         name=name,
#         gender=gender,
#         age=age,
#         countries=nation,
#     )

# def get_top_country(countries):
#     return max(countries, key=lambda c: c.probability)

# async def aggregate(name: str):
#     results = await asyncio.gather(
#         process_gender(name),
#         process_age(name),
#         process_nation(name),
#     )

#     gender, age, nation = results

#     return build_profile(name, gender, age, nation)
