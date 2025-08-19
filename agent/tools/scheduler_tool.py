from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any, Optional


class ScheduleRequest(BaseModel):
    content_id: str
    preferred_time: Optional[datetime] = None
    optimize: Optional[bool] = False

class ScheduleResponse(BaseModel):
    content_id: str
    scheduled_time: datetime
    status: str = Field(default="scheduled")

class SchedulerTool:
    name = "scheduler"
    description = "Schedule content posting at a specific or optimized time."

    def __init__(self):
        self.SCHEDULE_STORE: List[Dict] = []

    async def run(self, **kwargs) -> Dict[str, Any]:
        req = ScheduleRequest(**kwargs)

        # Decide time
        if req.optimize:
            scheduled_time = await self._get_best_post_time()
        elif req.preferred_time:
            scheduled_time = req.preferred_time
        else:
            raise ValueError("Must provide preferred_time or set optimize=True")

        # Save to storage
        await self._save_schedule(req.content_id, scheduled_time)

        # Return response
        res = ScheduleResponse(
            content_id=req.content_id,
            scheduled_time=scheduled_time
        )
        return res.model_dump()


    async def _get_best_post_time(self) -> datetime:
        """
        Simulate best post time selection based on past engagement data.
        Replace with real ML/statistical analysis later.
        """
        # Example: peak times: 10 AM, 6 PM
        now = datetime.now()
        peak_hours = [10, 18]
        best_hour = random.choice(peak_hours)
        best_time = now.replace(hour=best_hour, minute=0, second=0, microsecond=0)
        if best_time < now:
            best_time += timedelta(days=1)
        return best_time
    

    async def _save_schedule(self, content_id: str, scheduled_time: datetime):
        self.SCHEDULE_STORE.append({
            "content_id": content_id,
            "scheduled_time": scheduled_time
        })

    async def _get_schedules(self) -> List[Dict]:
        return self.SCHEDULE_STORE
