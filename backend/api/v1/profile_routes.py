from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

from agent.tools.profile_tool import Profile

router = APIRouter()

class ProfileResponse(BaseModel):
    status_code: int
    content: str
    user_id: str
    # profile: Profile

@router.get('/profile/{user_id}')
async def show_profile(user_id: str) -> ProfileResponse:
    try:
        # get data from db
        # profile_data = await db.fetch_profile(user_id=user_id)
        return ProfileResponse(
            status_code=200,
            content="Profile data fetched successfully",
            user_id=user_id,
            # profile=Profile(**profile_data)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post('/create_profile')
async def create_profile(profile: Profile) -> ProfileResponse:
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