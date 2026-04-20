from sqlalchemy.ext.asyncio import create_async_engine

from src.app.core.config import settings

DATABASE_URL = settings.database_url
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.debug,  # shows SQL queries in logs (optional)
)
