
"""The clock is a dependency: every time-based rule reads it."""

from datetime import datetime, timezone


def get_clock() -> datetime:
    return datetime(2026, 9, 27, 19, 10, tzinfo=timezone.utc)
