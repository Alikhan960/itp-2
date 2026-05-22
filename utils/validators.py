"""
utils/validators.py
Input validation utilities for EventHub.
"""

import re
from datetime import datetime


def validate_date(date_str: str) -> bool:
    """Check that date_str matches YYYY-MM-DD and is not in the past."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.date() >= datetime.now().date()
    except ValueError:
        return False


def validate_time(time_str: str) -> bool:
    """Check that time_str matches HH:MM."""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def validate_capacity(cap_str: str) -> bool:
    """Capacity must be a positive integer."""
    try:
        return int(cap_str) > 0
    except ValueError:
        return False


def validate_username(username: str) -> bool:
    """Username: 3-20 chars, alphanumeric + underscore."""
    return bool(re.match(r"^\w{3,20}$", username))


def validate_password(password: str) -> bool:
    """Password must be at least 6 characters."""
    return len(password) >= 6
