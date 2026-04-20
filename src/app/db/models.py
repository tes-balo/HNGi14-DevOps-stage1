import enum

from sqlalchemy import (
    INTEGER,
    TIMESTAMP,
    UUID,
    VARCHAR,
    Enum,
    Float,
    Integer,
    func,
    text,
)
from sqlalchemy.orm import mapped_column

from src.app.db.database import Base


class AgeGroupEnum(enum.Enum):
    ADULT = "Adult"
    TEENAGER = "Teenager"
    CHILD = "Child"
    SENIOR = "Senior"


class UserData(Base):
    __tablename__ = "user_profile"

    id = mapped_column(
        UUID,
        primary_key=True,
        index=True,
        server_default=text("uuidv7()"),
    )
    name = mapped_column(VARCHAR(128), nullable=False, index=True)
    gender = mapped_column(VARCHAR(32), nullable=False)
    gender_probability = mapped_column(Float, nullable=False)
    sample_size = mapped_column(INTEGER, nullable=False)
    age = mapped_column(Integer, nullable=False)
    age_group = mapped_column(Enum(AgeGroupEnum), nullable=False)
    country_id = mapped_column(VARCHAR(3), nullable=False)
    country_probability = mapped_column(Float, nullable=False)
    created_at = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
