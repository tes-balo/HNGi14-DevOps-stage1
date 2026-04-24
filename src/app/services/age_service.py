# from src.app.common.enums.age_group import AgeGroup
# from src.app.common.schemas.schema import (
#     AgeAPIResponse,
#     AgeResponse,
#     ExternalAPI,
# )
# from src.app.core.exceptions import ExternalAPIError
# from src.clients.agify.client import AgifyClient


# class AgeService:
#     """Service responsible for fetching and processing age predictions from an external API.

#     Acts as an adapter between the external age prediction service and the internal
#     application schema.
#     """

#     def __init__(self, client: AgifyClient):
#         self.client = client

#     async def process_age(self, name: str):
#         """Fetch age prediction data for a given name.

#         This method calls an external age prediction API, validates the response,
#         and converts it into the internal AgeResponse schema.

#         Args:
#             name (str): The name to analyze.

#         Returns:
#             AgeResponse: Structured age prediction containing:
#                 - name
#                 - estimated age
#                 - age group

#         Raises:
#             ExternalAPIError: If the API response is invalid or empty.

#         """
#         data: AgeAPIResponse = AgeAPIResponse(**(await self.client.get_age(name)))

#         if not data.age:
#             raise ExternalAPIError(ExternalAPI.AGIFY)

#         age_group = AgeGroup.classify_age_group(data.age)

#         return AgeResponse(
#             age=data.age,
#             age_group=age_group,
#         )


# def get_age_service() -> AgeService:
#     return AgeService(AgifyClient())
