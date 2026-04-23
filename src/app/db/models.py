from sqlalchemy import (
    TIMESTAMP,
    VARCHAR,
    Float,
    Integer,
    func,
)
from sqlalchemy.orm import mapped_column

from src.app.db.base_model import BaseModel


class UserData(BaseModel):
    __tablename__ = "user_profile"

    name = mapped_column(VARCHAR(128), nullable=False, unique=True)

    gender = mapped_column(VARCHAR(16), nullable=False)
    gender_probability = mapped_column(Float, nullable=False)

    age = mapped_column(Integer, nullable=False)
    age_group = mapped_column(VARCHAR(16), nullable=False)

    country_id = mapped_column(VARCHAR(2), nullable=False)
    country_name = mapped_column(VARCHAR(128))
    country_probability = mapped_column(Float, nullable=False)

    created_at = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
