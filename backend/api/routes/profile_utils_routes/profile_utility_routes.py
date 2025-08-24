from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from backend.db.models import UserProfile, Post, engine
from backend.api.routes.profile_utils_routes.util_functions import ProfileUtils

router = APIRouter()

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    linkedin_url: Optional[str] = None
    experience: Optional[Dict[str, Any]] = None
    skills: Optional[List[str]] = None
    
'''
    Route to delete a user profile by user ID.

    Args:
        user_id (int): The ID of the user profile to delete.
'''
@router.delete('/delete/{user_id}')
async def delete_user_profile(user_id: int):
    # Create an instance of ProfileUtils
    profile_utils = ProfileUtils()
    return await profile_utils.delete_profile(user_id=user_id)


'''
    Route to update a user profile by user ID.

    Args:
        user_id (int): The ID of the user profile to update.
        name (str, optional): The new name of the user.
        linkedin_url (str, optional): The new LinkedIn URL of the user.
        experience (Dict[str, Any], optional): The new experience details of the user.
        skills (List[str], optional): The new skills of the user.
        
        User can update any of the fields in their profile.
'''
@router.put('/update/{user_id}')
async def update_user_profile(user_id: int, req: UpdateProfileRequest):
    profile_utils = ProfileUtils()
    return await profile_utils.update_profile(
        user_id=user_id,
        name=req.name,
        linkedin_url=req.linkedin_url,
        experience=req.experience,
        skills=req.skills
    )
