from fastapi import HTTPException
from typing import List, Dict, Any, Optional
from sqlmodel import Session, select
from backend.db.models import UserProfile, Post, engine

class ProfileUtils:
    @staticmethod
    async def delete_profile(user_id: int) -> Dict[str, Any]:
        with Session(engine) as session:
            profile = session.exec(select(UserProfile).where(UserProfile.user_id == user_id)).first()
            if not profile:
                raise HTTPException(status_code=404, detail="User profile not found")
            session.delete(profile)
            session.commit()
            return {"message": "User profile deleted", "user_id": user_id}

    @staticmethod
    async def update_profile(
        user_id: int,
        name: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        experience: Optional[Dict[str, Any]] = None,
        skills: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        with Session(engine) as session:
            profile = session.exec(select(UserProfile).where(UserProfile.user_id == user_id)).first()
            if not profile:
                raise HTTPException(status_code=404, detail="User profile not found")
            if name is not None:
                profile.name = name
            if linkedin_url is not None:
                profile.linkedin_url = linkedin_url
            if experience is not None:
                profile.experience = experience
            if skills is not None:
                profile.skills = skills
            session.add(profile)
            session.commit()
            return {"message": "User profile updated", "user_id": user_id}
