from cProfile import Profile
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from sqlmodel import Session, select

# from agent.tools.profile_tool import Profile
from backend.db.models import UserProfile, engine  # Assuming you have a UserProfile model defined

router = APIRouter()

class ProfileResponse(BaseModel):
    status_code: int
    content: str
    user_id: int
    profile: Optional[UserProfile] = None  # Use UserProfile model directly

@router.get('/get_profile/{user_id}')
async def show_profile(user_id: int) -> ProfileResponse:
    try:
        # get data from db
        '''
        with Session(engine) as session:
            profile_data = session.exec(select(UserProfile).filter(UserProfile.user_id == user_id)).first()
            if not isinstance(profile_data, UserProfile):
                profile_data = UserProfile(**profile_data)  
            # Close the session
            session.close()
        '''        

        # return response
        return ProfileResponse(
            status_code=200,
            content="Profile data fetched successfully",
            user_id=user_id,
            # profile=profile_data
            profile=None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post('/create_profile')
async def create_profile(profile: UserProfile) -> ProfileResponse:
    try:
        # Store profile in the database
        # await db.store_profile(profile)

        # Simulate profile creation
        return ProfileResponse(
            status_code=201,
            content="User registered successfully",
            user_id=profile.user_id,
            # profile=profile
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))