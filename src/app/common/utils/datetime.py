from datetime import UTC, datetime


def to_iso8601_z(dt: datetime) -> str:
    """Convert datetime to ISO 8601 UTC format with Z suffix."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)

    dt = dt.astimezone(UTC)

    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")
