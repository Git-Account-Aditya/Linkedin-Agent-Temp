from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from sqlmodel import Session, select


from backend.db.models import Post, engine


router = APIRouter()

class ScheduledPosts(BaseModel):
    user_id: str
    posts: List[Dict[str, Any]]

@router.get("/scheduled_posts/{user_id}")
async def get_scheduled_posts(user_id: str) -> ScheduledPosts:
    # simulate database call
    
    # extract all scheduled posts of user(user_id)
    with Session(engine) as session:
        statement = select(Post).where(Post.user_id == user_id, Post.scheduled_for != None)
        results = session.exec(statement).all()

        session.close()

    '''
    In real case, Map the results to this desired format
    '''
    # posts = []

    # for result in results:
    #     posts.append({
    #         "content_id": str(result.post_id),
    #         "scheduled_time": result.scheduled_for,
    #         "status": "scheduled"
    #     })

    '''
    Map the results to this format for testing
    '''
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
