# utils/time.py
from datetime import UTC, datetime


def utc_now_iso():
    """Get the current UTC timestamp in ISO 8601 format.

    The returned string uses 'Z' to indicate UTC timezone,
    matching common API and specification requirements.

    Returns:
        str: Current UTC time formatted as 'YYYY-MM-DDTHH:MM:SSZ'.

    """
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
