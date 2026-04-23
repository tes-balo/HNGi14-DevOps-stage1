import uuid
from datetime import datetime
from enum import Enum
from typing import Generic, TypedDict, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from src.app.common.enums.age_group import AgeGroupEnum
from src.app.common.utils.datetime import to_iso8601_z


class ExternalAPI(str, Enum):
    GENDERIZE = "Genderize"
    AGIFY = "Agify"
    NATIONALIZE = "Nationalize"


# class AgeGroupEnum(str, Enum):
#     CHILD = "child"
#     TEENAGER = "teenager"
#     ADULT = "adule"
#     SENIOR = "senior"


class GenderAPIResponse(BaseModel):
    name: str
    gender: str | None
    probability: float = Field(ge=0, le=1)
    count: int


class AgeAPIResponse(BaseModel):
    count: int
    name: str
    age: int


class AgeResponse(BaseModel):
    age: int
    age_group: AgeGroupEnum


class CountryProbability(BaseModel):
    # normalized country_id to avoid 1:1 mapping to API
    country: str = Field(
        max_length=2,
        pattern="^[A-Z]{2,3}$",
        examples=["NG", "USA"],
    )
    probability: float = Field(ge=0, le=1)


class NationAPICountry(BaseModel):
    country_id: str
    probability: float


class NationAPIResponse(BaseModel):
    count: int | None = None
    name: str | None = None
    country: list[NationAPICountry]


class NationResponse(BaseModel):
    country_id: str = Field(
        max_length=2,
        pattern="^[A-Z]{2,3}$",
        examples=["NG", "USA"],
    )
    country_probability: float


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


class GenderResponse(BaseModel):
    name: str
    gender: str
    gender_probability: float = Field(ge=0, le=1)
    sample_size: int


class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, examples=["ella"])

    @field_validator("name")
    @classmethod
    def normalize_fields(cls, value: str):
        return value.lower()


class ProfileCreateGetResponse(BaseModel):
    id: uuid.UUID | None = None
    name: str
    gender: str
    gender_probability: float = Field(ge=0, le=1)

    sample_size: int
    age: int
    age_group: AgeGroupEnum
    country_id: str
    country_probability: int
    created_at: datetime | None = None

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime):
        return to_iso8601_z(value)


class ProfileAggregateResponse(BaseModel):
    name: str

    gender: GenderResponse
    age: AgeResponse
    countries: list[CountryProbability]
    # country_id: str
    # country_probability: float


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProfilesData(BaseModel):
    id: uuid.UUID
    name: str = Field(min_length=1, examples=["emmanuel"])
    gender: str
    age: int
    age_group: str
    country_id: str


# @field_validator("gender", "age_group")
# @classmethod
# def normalize_fields(cls, value: str):
#     return value.lower()`


# class SortEnum(str, Enum):
#     age = "age"
#     created_at = "created_at"
#     gender_probability = "gender_probability"


class OrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"


# to be used in repos.py for where clause
class AllProfilesFilters(TypedDict, total=False):
    gender: list[GenderEnum]
    age_group: AgeGroupEnum
    country_id: str
    min_age: int
    max_age: int
    min_gender_probability: float
    min_country_probability: float
    age: int


class SortEnum(str, Enum):
    age = "age"
    created_at = "created_at"
    gender_probability = "gender_probability"


# For order by
class SortParams(BaseModel):
    sort_by: SortEnum | None = None
    order: OrderEnum = OrderEnum.asc


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=50)


# to be used in services.py
from pydantic import BaseModel, Field


class ProfileFilters(BaseModel):
    gender: GenderEnum | None = None
    age_group: AgeGroupEnum | None = None
    country_id: str | None = Field(
        default=None,
        max_length=2,
        pattern="^[A-Z]{2}$",
        examples=["NG", "US"],
    )
    min_age: int | None = None
    max_age: int | None = None
    min_gender_probability: int | None = Field(default=None, ge=0, le=1)
    min_country_probability: int | None = Field(default=None, ge=0, le=1)


class AllProfilesQuery(BaseModel):
    filters: ProfileFilters = ProfileFilters()
    sort: SortParams = SortParams()
    pagination: PaginationParams = PaginationParams()


class AllProfilesResponse(BaseModel):
    status: str
    count: int
    data: ProfilesData


class ProfileDeleteResponse(BaseModel):
    pass


class HNGProfileData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    gender: GenderEnum
    gender_probability: float
    age: int
    age_group: AgeGroupEnum
    country_id: str
    country_name: str | None = None
    country_probability: float
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime):
        return to_iso8601_z(value)


class HNGProfileCreateData(BaseModel):
    name: str
    gender: str
    gender_probability: float
    sample_size: int
    age: int
    age_group: str
    country_id: str
    country_probability: float

    model_config = ConfigDict(from_attributes=True)


class HNGProfileResponse(BaseModel):
    status: str = Field(default="success")
    data: HNGProfileData


class ProfileExistsResponse(BaseModel):
    status: str
    message: str = "Profile already exists"
    data: HNGProfileData


class SeedData(TypedDict):
    name: str
    gender: str
    gender_probability: float
    age: int
    age_group: AgeGroupEnum
    country_id: str
    country_name: str
    country_probability: float


class ProfilesSeed(TypedDict):
    profiles: list[SeedData]


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated API response."""

    status: str = "success"
    page: int
    limit: int
    total: int
    data: list[T]

