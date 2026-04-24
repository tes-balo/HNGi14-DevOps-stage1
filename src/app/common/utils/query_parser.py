import re
from typing import Any

from pydantic import BaseModel

COUNTRY_MAP: dict[str, str] = {
    # West Africa
    "nigeria": "Nigeria",
    "ghana": "Ghana",
    "mali": "Mali",
    "senegal": "Senegal",
    "ivory coast": "Ivory Coast",
    "cote d'ivoire": "Ivory Coast",
    "burkina faso": "Burkina Faso",
    "benin": "Benin",
    "togo": "Togo",
    "niger": "Niger",
    "guinea": "Guinea",
    "sierra leone": "Sierra Leone",
    "liberia": "Liberia",
    # East Africa
    "kenya": "Kenya",
    "uganda": "Uganda",
    "tanzania": "Tanzania",
    "rwanda": "Rwanda",
    "burundi": "Burundi",
    "ethiopia": "Ethiopia",
    "somalia": "Somalia",
    "sudan": "Sudan",
    "south sudan": "South Sudan",
    "djibouti": "Djibouti",
    "eritrea": "Eritrea",
    # Southern Africa
    "south africa": "South Africa",
    "namibia": "Namibia",
    "botswana": "Botswana",
    "zimbabwe": "Zimbabwe",
    "zambia": "Zambia",
    "malawi": "Malawi",
    "mozambique": "Mozambique",
    "lesotho": "Lesotho",
    "eswatini": "Eswatini",
    # North Africa
    "egypt": "Egypt",
    "morocco": "Morocco",
    "algeria": "Algeria",
    "tunisia": "Tunisia",
    "libya": "Libya",
    # Europe (from your sample data)
    "united kingdom": "United Kingdom",
    "uk": "United Kingdom",
    "england": "United Kingdom",
    "france": "France",
    "germany": "Germany",
    "italy": "Italy",
    "spain": "Spain",
    # Americas (if dataset expands)
    "united states": "United States",
    "usa": "United States",
    "us": "United States",
    "canada": "Canada",
    "brazil": "Brazil",
}


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
    q = query.lower().strip()
    filters: dict[str, Any] = {}

    # -------------------------
    # GENDER (supports plural + multiple)
    # -------------------------
    genders: set[str] = set()

    if re.search(r"\b(male|males|man|men|boy|boys|guy|guys)\b", q):
        genders.add("male")

    if re.search(r"\b(female|females|woman|women|girl|girls|lady|ladies)\b", q):
        genders.add("female")

    if genders:
        filters["gender"] = list(genders)

    # -------------------------
    # AGE GROUP
    # -------------------------
    age_group_found = None

    # sort by length DESC so "youngsters" beats "young"
    for key in sorted(AGE_GROUP_KEYWORDS.keys(), key=len, reverse=True):
        if re.search(rf"(?<!\w){re.escape(key)}(?!\w)", q):
            age_group_found = AGE_GROUP_KEYWORDS[key]
            break

    if age_group_found:
        filters["age_group"] = age_group_found

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
    country_match = re.search(r"\b(from|in|of)\s+([a-zA-Z' ]{2,40})\b", q)

    if country_match:
        raw_country = country_match.group(2).strip().lower()

        # remove filler words
        raw_country = re.sub(r"\b(the|a|an)\b", "", raw_country).strip()

        normalized = COUNTRY_MAP.get(raw_country)

        if normalized:
            filters["country_name"] = normalized
        else:
            filters["country_name"] = raw_country.title()
        # -------------------------
    # -------------------------
    # COMPOUND LOGIC FIXES (IMPORTANT)
    # -------------------------

    # default age_group inference only if nothing else is set
    if "age_group" not in filters:
        if "adult" in q:
            filters["age_group"] = "adult"
        elif "teen" in q or "teenager" in q:
            filters["age_group"] = "teenager"

    # "people" should NOT imply gender
    if re.search(r"\bpeople\b", q):
        filters.pop("gender", None)

    # 🔥 CRITICAL FIX: any numeric age filter overrides age_group
    if any(k in filters for k in ["age", "min_age", "max_age"]):
        filters.pop("age_group", None)

    # remove contradictions: age overrides age_group
    if "age" in filters:
        filters.pop("age_group", None)

    return ParsedQuery(
        filters=filters,
        page=page,
        limit=limit,
    )
