import re
from typing import Any

from pydantic import BaseModel


class ParsedQuery(BaseModel):
    filters: dict[str, Any]
    page: int = 1
    limit: int = 10


MALE_KEYWORDS = {
    # most common
    "male",
    "man",
    "men",
    "boy",
    "boys",
    "guy",
    "guys",
    # moderately common
    "gentleman",
    "gentlemen",
    "lad",
    "lads",
    "dude",
    "dudes",
    "him",
    "his",
    # less common
    "bloke",
    "blokes",
    "chap",
    "chaps",
    "gent",
    "gents",
}

FEMALE_KEYWORDS = {
    # most common
    "female",
    "woman",
    "women",
    "girl",
    "girls",
    "lady",
    "ladies",
    # moderately common
    "gal",
    "gals",
    "gurls",
    "her",
    "hers",
    "miss",
    "mrs",
    "ms",
    # less common
    "lass",
    "lasses",
    "dame",
    "dames",
    "madam",
}

AGE_GROUP_KEYWORDS = {
    # child
    "kid": "child",
    "kids": "child",
    "child": "child",
    "children": "child",
    # teenager
    "teen": "teenager",
    "teens": "teenager",
    "teenager": "teenager",
    "teenagers": "teenager",
    "adolescent": "teenager",
    "adolescents": "teenager",
    "young": "teenager",
    "youngster": "teenager",
    "youngsters": "teenager",
    "junior": "teenager",
    "bro": "teenager",
    "sis": "teenager",
    # adult
    "adult": "adult",
    "adults": "adult",
    "grownup": "adult",
    "grownups": "adult",
    "middle-aged": "adult",
    "youth": "adult",
    "egbon": "adult",
    "agba": "adult",
    "agbalagba": "adult",
    # senior
    "old": "senior",
    "older": "senior",
    "elder": "senior",
    "elders": "senior",
    "elderly": "senior",
    "senior": "senior",
    "seniors": "senior",
    "aged": "senior",
    "pensioner": "senior",
    "pensioners": "senior",
    "retiree": "senior",
    "retirees": "senior",
}

AGE_GROUP_RANGES = {
    "child": (0, 12),
    "teenager": (13, 24),
    "adult": (24, 59),
    "senior": (65, 120),
}


# def parse_query(query: str) -> dict[str, Any]:
#     tokens = query.lower().split()
#     filters: dict[str, Any] = {}
#     genders: list[str] = []

#     for token in tokens:
#         clean = token.strip(".,!?")

#         if clean in MALE_KEYWORDS:
#             genders.append("male")

#         if clean in FEMALE_KEYWORDS:
#             genders.append("female")

#         if clean in AGE_GROUP_KEYWORDS:
#             age_group = AGE_GROUP_KEYWORDS[clean]
#             filters["age_group"] = age_group

#             if age_group not in AGE_GROUP_RANGES:
#                 raise ValueError(f"Age group '{age_group}' has no range defined")

#             min_age, max_age = AGE_GROUP_RANGES[age_group]
#             filters["min_age"] = min_age
#             filters["max_age"] = max_age

#         elif clean.isdigit():
#             age = int(clean)
#             filters["age"] = age

#     if genders:
#         filters["gender"] = list(set(genders))

#     return filters


from typing import Any


def parse_query(query: str, page: int = 1, limit: int = 10) -> ParsedQuery:
    q = query.lower().strip()
    filters: dict[str, Any] = {}

    # -------------------------
    # GENDER (supports plural + multiple)
    # -------------------------
    genders: set[str] = set()

    if re.search(r"\b(male|man|men|boy|boys|guy|guys)\b", q):
        genders.add("male")

    if re.search(r"\b(female|woman|women|girl|girls|lady|ladies)\b", q):
        genders.add("female")

    if genders:
        filters["gender"] = sorted(list(genders))

    # -------------------------
    # AGE GROUP
    # -------------------------
    for key, group in AGE_GROUP_KEYWORDS.items():
        if key in q:
            filters["age_group"] = group
            break

    # -------------------------
    # AGE COMPARISONS (STRICT FIX)
    # -------------------------

    # "above 30"
    match = re.search(r"\babove\s+(\d{1,3})\b", q)
    if match:
        filters["min_age"] = int(match.group(1))

    # "below 30"
    match = re.search(r"\bbelow\s+(\d{1,3})\b", q)
    if match:
        filters["max_age"] = int(match.group(1))

    # "older than 30" (important test cases!)
    match = re.search(r"\b(older|greater|over)\s+than\s+(\d{1,3})\b", q)
    if match:
        filters["min_age"] = int(match.group(2))

    # DO NOT allow raw age override unless explicit "age is 30"
    if re.search(r"\bage\s+is\s+\d{1,3}\b", q):
        filters["age"] = int(re.findall(r"\d{1,3}", q)[0])

    # -------------------------
    # COUNTRY (FIXED FOR SEED JSON)
    # -------------------------
    match = re.search(r"\bfrom\s+([a-zA-Z ]+)\b", q)
    if match:
        country = match.group(1).strip().lower()

        # normalize spacing
        filters["country_name"] = country

    # -------------------------
    # COMPOUND LOGIC FIXES
    # -------------------------

    if "young" in q and "min_age" not in filters and "max_age" not in filters:
        filters.setdefault("age_group", "teenager")

    if "adult" in q:
        filters.setdefault("age_group", "adult")

    if "teenager" in q or "teen" in q:
        filters["age_group"] = "teenager"

    # resolve conflicts between age_group and numeric age filters
    if "min_age" in filters or "max_age" in filters:
        filters.pop("age_group", None)

    return ParsedQuery(
        filters=filters,
        page=page,
        limit=limit,
    )
