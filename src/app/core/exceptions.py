# from enum import Enum

# from fastapi import HTTPException, status


# class ExternalAPI(str, Enum):
#     GENDERIZE = "Genderize"
#     AGIFY = "Agify"
#     NATIONALIZE = "Nationalize"


# class ExternalAPIError(HTTPException):
#     """Generic wrapper for any external dependency failure."""

#     def __init__(self, api: ExternalAPI, message: str | None = None) -> None:

#         detail = {
#             "status": "error",
#             "message": message or f"{api} returned an invalid response.",
#         }

#         # status_code = status.HTTP_502_BAD_GATEWAY
#         super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)


from src.app.common.schemas.schema import ExternalAPI


class ExternalAPIError(Exception):
    def __init__(self, api_name: ExternalAPI, message: str | None = None):
        self.api_name = api_name
        self.message = message or f"{api_name.value} returned an invalid response"


class NotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass
