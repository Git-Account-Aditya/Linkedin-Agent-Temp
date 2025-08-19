from fastapi import APIRouter, HTTPException
from typing import Any, List, Dict   
from pydantic import BaseModel
from datetime import datetime, timezone

from agent.orchestrator.orchestrator import Post
from backend.api.v1.profile_routes import show_profile, ProfileResponse

router = APIRouter()

# class Post(BaseModel):
#     id: Optional[str] = None
#     user_id: str
#     text: str
#     created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
#     scheduled_for: Optional[datetime] = None
#     metadata: Dict[str, Any] = Field(default_factory=dict)

class ContentJSON(BaseModel):
    id: str
    user_id: str
    message: str
    content: Dict[str, Post]

@router.post('/delete_content/{content_id}')
async def delete_content(content_id: str) -> Dict[str, Any]:
    try:
        # Simulate content deletion
        return {"status": "content deleted successfully",
                "message": f"Content with ID {content_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))             


@router.get('/fetch_content/{user_id}')
async def fetch_content(user_id: str) -> ContentJSON:
    try:
        # Simulate fetching content
        data = await show_profile(user_id)
        if isinstance(data, ProfileResponse):
            profile = data.profile if hasattr(data, 'profile') else None
            raw_content = profile.raw if profile else {}

            posts = raw_content.get('posts', [])

            data = {
                "id": user_id,
                "user_id": user_id,
                "message": "Content fetched successfully",
                "content": {str(i): Post(**post) for i, post in enumerate(posts)}
            }
            return ContentJSON(**data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
