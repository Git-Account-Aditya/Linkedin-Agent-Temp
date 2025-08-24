from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

class linkedinapi:
    def __init__(self, api):
        self.api = api

    '''Fetch LinkedIn profile information (used in profile tool)'''
    async def get_profile(self, user_id: str):
        # Simulate fetching a LinkedIn profile

        # demo return as linkedin does not allow its API to be used for learning purposes
        return {
            "user_id": user_id,
            "name": "John Doe",
            "linkedin_url": "https://www.linkedin.com/in/JohnDoe",
            "experience": {"Salesforce": "3 years"},
            "skills": ["Python", "Machine Learning", "Data Analysis"],
            "posts": [
                {
                    "post_id": 1,
                    "user_id": 1002,    
                    "content": "Excited to start my new role at Salesforce!",
                    "created_at": datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
                    "scheduled_for": datetime(2023, 1, 2, 12, 0, 0, tzinfo=timezone.utc),
                    "updated_at": [datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc).isoformat()]                    
                },
                {
                    "post_id": 2,
                    "user_id": 1002,
                    "content": "Just completed a project on AI-driven sales analytics.",
                    "created_at": datetime(2023, 1, 3, 12, 0, 0, tzinfo=timezone.utc),
                    "scheduled_for": datetime(2023, 1, 4, 12, 0, 0, tzinfo=timezone.utc),
                    "updated_at": [datetime(2023, 1, 3, 12, 0, 0, tzinfo=timezone.utc).isoformat()]
                }
            ]
        }
    

    '''Publish a post on LinkedIn (used in post tool)'''
    async def publish_post(self, user_id: int, content: str, media_urls: Optional[List[str]] = None,
                           visibility: str = 'visibility', tags: Optional[List[str]] = None) -> Dict[str, Any]:
        
        # Simulate publishing a post on LinkedIn
        
        # demo return as linkedin does not allow its API to be used for learning purposes
        post_id = 100230

        return {            
            "post_id": post_id,
            "url": f"https://www.linkedin.com/posts/user_id={user_id}&post_id={post_id}",
            "content": content,
            "media_urls": media_urls or [],
            "status": "published"
        }

