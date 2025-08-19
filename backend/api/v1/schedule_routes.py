from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List, Optional


router = APIRouter()

class ScheduledPosts(BaseModel):
    user_id: str
    posts: List[Dict[str, Any]]

@router.get("/scheduled_posts/{user_id}")
async def get_scheduled_posts(user_id: str) -> ScheduledPosts:
    # simulate database call

    posts = [
        {
            "content_id": "1",
            "scheduled_time": "2023-10-01T10:00:00Z",
            "status": "scheduled"
        },
        {
            "content_id": "2",
            "scheduled_time": "2023-10-02T11:00:00Z",
            "status": "scheduled"
        },
    ]
    return ScheduledPosts(user_id=user_id, posts=posts)
