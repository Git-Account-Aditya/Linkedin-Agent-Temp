# profile_tool.py
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser

# File imports
from ..prompts.analyze_profile_prompts import (
    profile_keyword_analysis_prompt,
    profile_activity_level_prompt,
)

from backend.db.models import UserProfile  # assuming you have a UserProfile model defined
# from ..llm import llm  # assuming you have an llm object somewhere
# from ..integrations.linkedin_api import linkedin_api  # hypothetical API client

load_dotenv()


class ProfileScrapTool:
    """
    Dynamic-agent compatible LinkedIn profile fetch + analysis tool.
    """

    name = "profile"
    description = (
        "Fetches a LinkedIn profile for the given user_id and analyzes it "
        "to extract top keywords and activity level."
    )

    def __init__(self, linkedin_api, llm):
        self.linkedin_api = linkedin_api
        self.llm = llm

    async def run(self, **kwargs) -> Dict[str, Any]:
        """
        Required for dynamic orchestrator.
        Args in kwargs:
            user_id (str): LinkedIn user ID.
        Returns:
            dict: {
                "profile": { ...profile fields... },
                "analysis": {
                    "top_keywords": [...],
                    "activity_level": int
                }
            }
        """
        user_id = kwargs.get("user_id")
        if not user_id:
            raise ValueError("Missing required argument: user_id")

        # Step 1: Fetch raw profile
        data = await self.linkedin_api.get_profile(user_id)  # sync call in your example

        profile = UserProfile(
            user_id=data.get("user_id"),
            name=data.get("name"),
            linkedin_url=data.get("linkedin_url"),
            experience=data.get("experience"),
            skills=data.get("skills"),
            raw=data,
            posts=data.get('posts')
        )

        # Step 2: Analyze profile
        # analysis = await self.analyze_profile(profile)
        analysis = {
            "top_keywords": ['artificial intelligence', 'business', 'content creation'],
            "activity_level": 6
        }

        # Step 3: Return combined result
        return {
            "profile": profile.model_dump(),
            "analysis": analysis,
        }

    async def analyze_profile(self, profile: UserProfile) -> Dict[str, Any]:
        """
        Runs keyword extraction and activity level scoring using LLM prompts.
        """
        # Keyword extraction
        keyword_chain = profile_keyword_analysis_prompt() | self.llm() | StrOutputParser()

        keywords = await keyword_chain.ainvoke(
            {
                "skills": profile.skills or [],
                "experience": profile.experience or {},
            }
        )

        # Activity level
        recent_post_time_str = (
            profile.raw.get("recent_post", {}).get("created_at")
            if profile.raw.get("recent_post")
            else None
        )
        no_of_posts = profile.raw.get("post_count", 0)

        recent_post_time = None
        if recent_post_time_str:
            try:
                recent_post_time = datetime.fromisoformat(recent_post_time_str)
            except ValueError:
                recent_post_time = None

        activity_chain = profile_activity_level_prompt() | self.llm() | StrOutputParser()

        activity_level = await activity_chain.ainvoke(
            {
                "recent_post_time": recent_post_time.isoformat() if recent_post_time else None,
                "no_of_posts": no_of_posts,
            }
        )

        return {
            "top_keywords": keywords if keywords else [],
            "activity_level": activity_level,
        }


    