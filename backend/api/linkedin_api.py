from typing import List, Optional, Dict, Any


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
            "experience": {"Salesforce": "3 years"},
            "skills": ["Python", "Machine Learning", "Data Analysis"]
        }

    '''Publish a post on LinkedIn (used in post tool)'''
    async def publish_post(self, user_id: str, content: str, media_urls: Optional[List[str]] = None,
                           visibility: str = 'visibility', tags: Optional[List[str]] = None) -> Dict[str, Any]:
        
        # Simulate publishing a post on LinkedIn
        
        # demo return as linkedin does not allow its API to be used for learning purposes
        post_id = 100230

        return {
            "post_id": post_id,
            "url": f"https://www.linkedin.com/posts/{post_id}",
            "content": content,
            "media_urls": media_urls or [],
            "status": "published"
        }

