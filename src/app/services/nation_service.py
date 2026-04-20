from src.app.common.schemas.schema import (
    CountryProbability,
    ExternalAPI,
    NationAPIResponse,
)
from src.app.core.exceptions import ExternalAPIError
from src.clients.nationalize.client import NationalizeClient


class NationService:
    """Service responsible for fetching and processing nationality predictions from an external API.

    This service converts raw responses from the Nationalize API into internal domain models
    for further aggregation.
    """

    def __init__(self, client: NationalizeClient):
        self.client = client

    async def process_nation(self, name: str) -> list[CountryProbability]:
        """Fetch nationality prediction data for a given name.

        This method calls the external nationality API, validates the response,
        and maps it into a list of internal CountryProbability objects.

        Args:
            name (str): The name to analyze.

        Returns:
            list[CountryProbability]: List of country probability predictions.

        Raises:
            ExternalAPIError: If the API returns no valid nationality data.

        """
        data = NationAPIResponse(**(await self.client.get_nation(name)))

        if not data.country:
            raise ExternalAPIError(ExternalAPI.NATIONALIZE)

        # top_country = max(data.country, key=lambda c: c.probability)
        # top_probability = top_country.probability

        return [
            CountryProbability(
                country=item.country_id,
                probability=item.probability,
            )
            for item in data.country
        ]


def get_nation_service() -> NationService:
    return NationService(NationalizeClient())
