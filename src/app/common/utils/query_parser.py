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


def parse_query(query: str, page: int = 1, limit: int = 10) -> ParsedQuery:
    """Converts natural language query into structured filters + pagination."""
    tokens = query.lower().split()
    filters: dict[str, Any] = {}
    genders: list[str] = []

    for token in tokens:
        clean = token.strip(".,!?")

        # gender
        if clean in MALE_KEYWORDS:
            genders.append("male")

        if clean in FEMALE_KEYWORDS:
            genders.append("female")

        # age group
        if clean in AGE_GROUP_KEYWORDS:
            age_group = AGE_GROUP_KEYWORDS[clean]
            filters["age_group"] = age_group

            if age_group in AGE_GROUP_RANGES:
                min_age, max_age = AGE_GROUP_RANGES[age_group]
                filters["min_age"] = min_age
                filters["max_age"] = max_age

        # numeric age like "30"
        elif clean.isdigit():
            filters["age"] = int(clean)

    # gender dedupe
    if genders:
        filters["gender"] = list(set(genders))

    return ParsedQuery(
        filters=filters,
        page=page,
        limit=limit,
    )
