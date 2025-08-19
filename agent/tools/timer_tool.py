from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Union, Sequence

from pydantic import BaseModel, Field

from .utils import humanize_timedelta, parse_datetime_like


class TimerRequest(BaseModel):
    # Accept ISO 8601 string or datetime
    scheduled_time: Union[str, datetime] = Field(..., description="Target time to post (ISO8601 or datetime).")
    now: Optional[Union[str, datetime]] = Field(None, description="Override current time (ISO8601 or datetime).")
    humanize: bool = Field(default=True, description="Return a human-readable duration string.")
    granularity: Sequence[str] = Field(default=("days", "hours", "minutes"), description="Units to include in humanized output.")
    clamp_zero: bool = Field(default=True, description="If True, negative deltas return 0 seconds when overdue.")


class TimerResponse(BaseModel):
    scheduled_time_iso: str
    now_iso: str
    seconds_remaining: int
    overdue: bool
    humanized: Optional[str] = None


class TimerTool:
    name = "timer"
    description = "Compute time remaining until a scheduled time; returns seconds and a human-readable string."

    async def run(self, **kwargs) -> Dict[str, Any]:
        req = TimerRequest(**kwargs)

        now_dt = parse_datetime_like(req.now) if req.now is not None else datetime.now(timezone.utc)
        sched_dt = parse_datetime_like(req.scheduled_time)

        # Normalize both to timezone-aware
        if sched_dt.tzinfo is None:
            sched_dt = sched_dt.replace(tzinfo=timezone.utc)
        if now_dt.tzinfo is None:
            now_dt = now_dt.replace(tzinfo=timezone.utc)

        delta = sched_dt - now_dt
        total_seconds = int(delta.total_seconds())
        overdue = total_seconds < 0
        seconds_remaining = 0 if (req.clamp_zero and overdue) else total_seconds

        humanized: Optional[str] = None
        if req.humanize:
            humanized = humanize_timedelta(delta, granularity=req.granularity)

        res = TimerResponse(
            scheduled_time_iso=sched_dt.isoformat(),
            now_iso=now_dt.isoformat(),
            seconds_remaining=seconds_remaining,
            overdue=overdue,
            humanized=humanized,
        )
        return res.model_dump()