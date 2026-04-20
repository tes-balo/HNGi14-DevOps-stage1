# utils/id.py
import uuid_utils


def generate_id() -> uuid_utils.UUID:
    """Generate a unique identifier for a profile.

    Uses UUIDv7 for time-ordered, globally unique IDs suitable for databases.

    Returns:
        uuid.UUID: A new UUIDv7 identifier.

    """
    return uuid_utils.uuid7()
