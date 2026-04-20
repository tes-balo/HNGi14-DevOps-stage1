import httpx


# TODO@tes-balo: Refactor to reuse http layer later
class BaseAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get(self, endpoint: str, params: dict[str, str] | None = None):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=5.0,
            )
            print("URL:", response.url)
            print("STATUS:", response.status_code)
            print("BODY:", response.text)
            response.raise_for_status()
            if not response.content:
                raise RuntimeError(
                    f"Empty response from {response.url}",
                )

            try:
                return response.json()
            except ValueError:
                raise RuntimeError(
                    f"Invalid JSON from {response.url}. "
                    f"Status={response.status_code}, Body={response.text[:200]}",
                )
