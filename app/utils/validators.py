"""
Validation helpers
- Used across routes & services
"""

import re


EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def is_email(value: str) -> bool:
    return bool(value and EMAIL_REGEX.match(value))


def min_length(value: str, length: int) -> bool:
    return isinstance(value, str) and len(value.strip()) >= length


def required_fields(data: dict, fields: list[str]):
    """
    Ensure required fields exist and are not empty
    Returns (ok, missing_fields)
    """
    missing = [f for f in fields if not data.get(f)]
    return len(missing) == 0, missing
