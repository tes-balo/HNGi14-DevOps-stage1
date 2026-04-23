import uuid_utils
from sqlalchemy import TIMESTAMP, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.app.db.database import Base


def uuid7():
    return str(uuid_utils.uuid7())


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid7)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
    )
