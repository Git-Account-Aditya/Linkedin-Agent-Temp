from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, AnyUrl
from sqlmodel import Session, select, Column, JSON

# from agent.tools.profile_tool import Profile
from backend.db.models import UserProfile, Post, engine  # Assuming you have a UserProfile model defined

router = APIRouter()

class ProfileResponse(BaseModel):
    status_code: int
    content: str
    user_id: int
    profile: Optional[UserProfile] = None  # Use UserProfile model directly


# Pydantic class for creating a profile
class ProfileCreateRequest(BaseModel):
    name: str
    linkedin_url: str

@router.get('/get_profile/{user_id}')
async def show_profile(user_id: int) -> ProfileResponse:
    try:
        # get data from db
        
        with Session(engine) as session:
            profile_data = session.exec(select(UserProfile).filter(UserProfile.user_id == user_id)).first()
            if not isinstance(profile_data, UserProfile):
                profile_data = UserProfile(**profile_data)  
            # Close the session
            session.close()
                

        # return response
        return ProfileResponse(
            status_code=200,
            content="Profile data fetched successfully",
            user_id=user_id,
            # profile=profile_data.model_dump()
            profile=profile_data.model_dump()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post('/create_profile/', response_model = ProfileResponse)
async def create_profile(request_body: ProfileCreateRequest):
    try:
        # Create a new user profile
        profile = UserProfile(
            name=request_body.name,
            linkedin_url=request_body.linkedin_url
        )

        # Store profile in the database
        with Session(engine) as session:
            session.add(profile)
            session.commit()
            session.refresh(profile)  # Refresh to get the updated profile with user_id
            # session.close()

        print('Profile created successfully')

        # Simulate profile creation
        return ProfileResponse(
            status_code=201,
            content="User registered successfully",
            user_id=profile.user_id,
            profile=profile
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


