from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Optional, Sequence, Union

def parse_datetime_like(value: Union[str, datetime]) -> datetime:
    """
    Parse ISO 8601 strings (supports 'Z' suffix) or pass-through datetime.
    Returns naive datetime as-is; caller should make timezone-aware if desired.
    """
    if isinstance(value, datetime):
        return value
    s = value.strip()
    # Allow 'Z' as UTC designator
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(s)
    except Exception:
        # Fallback: try without microseconds or spaces
        return datetime.fromisoformat(s.replace(" ", "T"))

def humanize_timedelta(delta: timedelta, granularity: Sequence[str] = ("days", "hours", "minutes")) -> str:
    """
    Humanize a timedelta into 'Xd Yh Zm' style; includes 'ago' if negative.
    """
    neg = delta.total_seconds() < 0
    seconds = abs(int(delta.total_seconds()))

    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    parts = []
    if "days" in granularity and days:
        parts.append(f"{days}d")
    if "hours" in granularity and hours:
        parts.append(f"{hours}h")
    if "minutes" in granularity and minutes:
        parts.append(f"{minutes}m")
    if "seconds" in granularity and not parts and seconds:
        parts.append(f"{seconds}s")

    if not parts:
        parts = ["0s"]

    text = " ".join(parts)
    return f"{text} ago" if neg else text