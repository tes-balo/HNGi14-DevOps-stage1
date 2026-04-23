import json
from pathlib import Path
from typing import Any


def load_country_mapping() -> dict[str, str]:
    mapping: dict[str, Any] = {}
    # Update this path to where your JSON file actually lives
    json_path = Path(__file__).parent.parent.parent.parent / "seed_data.json"

    try:
        if json_path.exists():
            with open(json_path) as f:
                data = json.load(f)
                for profile in data.get("profiles", []):
                    name = profile.get("country_name")
                    cid = profile.get("country_id")
                    if name and cid:
                        # Map lowercase name to ID for case-insensitive matching
                        mapping[name.lower()] = cid
    except Exception as e:
        # Fallback for local development if file is missing
        print(f"Warning: Could not load country mapping: {e}")

    return mapping


# This executes once when the app starts
COUNTRY_MAP = load_country_mapping()
