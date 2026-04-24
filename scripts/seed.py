import asyncio
import json
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.schemas.schema import ProfilesSeed, SeedData
from src.app.db.session import AsyncSessionLocal
from src.app.repos.repos import UserRepository

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR.parent / "data" / "seed_profiles.json"
with Path.open(file_path) as f:
    profiles_json_data = json.load(f)


# TODO: REFACTOR LATER TO USE repo.bulk_insert(profiles) which is much faster
async def seed_profiles(data: ProfilesSeed, db: AsyncSession):
    repo = UserRepository(db)
    profiles: list[SeedData] = data["profiles"]

    print(f"---------{profiles[:2]}--------")
    for profile in profiles:
        if not profile:
            continue
        # await repo.create_users_from_json(profile)

        await repo.create_users_from_json(profile)  # type: ignore  # noqa: PGH003
    await db.commit()
    print("Database seeding complete")


async def main():
    async with AsyncSessionLocal() as db:
        await seed_profiles(profiles_json_data, db)


if __name__ == "__main__":
    asyncio.run(main())
