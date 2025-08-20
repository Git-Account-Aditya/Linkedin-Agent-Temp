from fastapi import APIRouter, HTTPException
from typing import Any, List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime, timezone
from sqlmodel import Session, select


from backend.db.models import Post, engine
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
    user_id: str
    message: str
    content: Optional[Dict[str, Post]]

@router.post('/delete_content/{content_id}')
async def delete_content(content_id: int) -> Dict[str, Any]:
    try:
        # Simulate content deletion
        with Session(engine) as session:
            statement = select(Post).where(Post.post_id == content_id)
            post = session.exec(statement).first()
            if post:
                session.delete(post)
                session.commit()
                session.close()

                return {"status": "content deleted successfully",
                        "message": f"Content with ID {content_id} deleted successfully"}                
            else:
                raise HTTPException(status_code=404, detail="Content not found")           
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))             


@router.get('/fetch_content/{user_id}')
async def fetch_content(user_id: str) -> ContentJSON:
    try:
        # Simulate fetching content
        data = await show_profile(user_id)
        if isinstance(data, ProfileResponse):
            profile = data.profile if hasattr(data, 'profile') else None            

            posts = profile.posts if profile else {}

            data={
                "user_id": user_id,
                "message": "Content fetched successfully",
                "content": {str(i): Post(**post) for i, post in enumerate(posts)}
            }
            return ContentJSON(**data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
