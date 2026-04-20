from src.app.common.schemas.schema import ExternalAPI, GenderAPIResponse, GenderResponse
from src.app.core.exceptions import ExternalAPIError
from src.clients.genderize.client import GenderizeClient


class GenderService:
    """Service responsible for fetching and processing gender predictions from an external API.

    This service acts as an adapter between the external Genderize API and the internal
    application schema, ensuring consistent data formatting and validation.
    """

    def __init__(self, client: GenderizeClient):
        self.client = client

    async def process_gender(self, name: str):
        """Fetch gender prediction data for a given name.

        This method calls the external gender prediction API, validates the response,
        and maps it into the internal GenderResponse schema.

        Args:
            name (str): The name to analyze.

        Returns:
            GenderResponse: Structured gender prediction containing:
                - name
                - gender
                - gender probability
                - sample size

        Raises:
            ExternalAPIError: If the API returns invalid or insufficient data.

        """
        data = GenderAPIResponse(
            **(await self.client.get_gender(name)),
        )

        if not data.gender or data.count == 0:
            raise ExternalAPIError(ExternalAPI.GENDERIZE)

        return GenderResponse(
            name=data.name,
            gender=data.gender,
            gender_probability=data.probability,
            sample_size=data.count,
        )


def get_gender_service() -> GenderService:
    return GenderService(GenderizeClient())
