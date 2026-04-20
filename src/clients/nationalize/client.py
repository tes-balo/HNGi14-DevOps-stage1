import httpx
from fastapi import HTTPException, status

from src.clients.base import BaseAPIClient


class NationalizeClient(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url="https://api.nationalize.io/")

    async def get_nation(self, name: str):
        try:
            return await self.get("", {"name": name})
        except httpx.RequestError as e:
            print("🔥 ORIGINAL ERROR:", repr(e))
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={"status": "error", "message": "Upstream or server failure"},
            ) from e

        except httpx.HTTPStatusError as e:
            print("🔥 ORIGINAL ERROR:", repr(e))
            print("🔥 RESPONSE:", e.response.text)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={
                    "status": "error",
                    "message": "Upstream or server failure",
                },
            ) from e
