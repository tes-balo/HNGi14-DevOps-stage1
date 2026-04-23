# Profile API — README

## Overview
This project is a FastAPI-based profile management API that supports:
- Structured filtering (gender, age group, country, etc.)
- Natural language query parsing
- Sorting and pagination
- Profile search via both structured and natural language input

---

## Natural Language Parsing Approach

The system includes a lightweight query parser (`parse_query`) that converts free-text input into structured filters.

### Supported Keywords

#### Gender keywords
Mapped to:
- `male`
- `female`

**Examples:**
- "men", "boys", "guys", "male" → `gender = male`
- "women", "girls", "ladies", "female" → `gender = female`

If multiple gender keywords appear, both are included as a list filter.

---

#### Age group keywords
Mapped into standardized age groups:

| Keyword Group | Mapped Value |
|--------------|-------------|
| child, kids, children | `child` |
| teen, teenager, young | `teenager` |
| adult, grownup | `adult` |
| old, elderly, senior | `senior` |

Additionally, numeric inference is supported:
- If a number is detected (e.g. "24"), it is treated as exact age filter

---

#### Age range mapping
When an age group is detected:

- child → 0–12
- teenager → 13–24
- adult → 24–59
- senior → 65–120

These translate into:
- `min_age`
- `max_age`

---

### How Parsing Works

1. Query is lowercased
2. Split into tokens
3. Each token is checked against:
   - gender keyword set
   - age group keyword set
   - numeric values
4. Filters are accumulated into a dictionary:
   ```python
   {
     "gender": ["male"],
     "age_group": "teenager",
     "min_age": 13,
     "max_age": 24
   }
   ```

5. Returned as `ParsedQuery` object containing:
   - filters
   - page
   - limit

---

## Sorting & Pagination

Sorting is handled separately in the service layer:

Supported sort fields:
- `age`
- `created_at`
- `gender_probability`

Order:
- `asc`
- `desc`

Pagination:
- `page` (default = 1)
- `limit` (default = 10)

Offset calculation:
```
offset = (page - 1) * limit
```

---

## API Endpoints

### GET /api/profiles
Structured filtering endpoint.

Query params:
- gender
- age_group
- country_id
- min_age / max_age
- sorting
- pagination

---

### GET /api/profiles/search
Natural language search endpoint.

Example:
```
/api/profiles/search?q=men younger than 24
```

---

## Limitations

### 1. Basic NLP parsing
The parser is token-based only:
- No sentence structure understanding
- No context awareness
- No semantic interpretation

Example it cannot properly handle:
- "men not older than 24 living in Nigeria" (partial parsing only)

---

### 2. Limited phrase handling
Multi-word expressions are not supported:
- "under 24 years old" is partially parsed
- words are split into tokens only

---

### 3. No negation handling
Unsupported:
- "not male"
- "exclude seniors"
- "except women"

---

### 4. No country inference
Country names must match database fields exactly:
- No fuzzy matching
- No alias mapping

---

### 5. Age ambiguity
- "young" is mapped to teenager by default
- Context like "young adult" is not differentiated

---

### 6. Strict enum validation
Age group values are strict:
- CHILD
- TEENAGER
- ADULT
- SENIOR

Case mismatch (e.g. "adult" vs "ADULT") can cause validation errors depending on schema enforcement.

---

## Design Philosophy

This system prioritizes:
- Simplicity over NLP complexity
- Predictability over flexibility
- Structured filtering over semantic reasoning

---

## Summary

The API acts as a hybrid system:
- Structured query API for precision
- Lightweight NLP parser for convenience search

It is intentionally minimal to ensure performance and reliability in production environments.
