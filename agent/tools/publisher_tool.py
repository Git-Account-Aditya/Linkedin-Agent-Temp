from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class PublishRequest(BaseModel):
    user_id: str = Field(..., description="Owner of the content to publish")
    content: str = Field(..., description="Text content for the post")
    media_urls: Optional[List[HttpUrl]] = Field(default=None, description="Optional media URLs to attach")
    visibility: str = Field(default="connections", description="Post visibility: public|connections|private")
    tags: Optional[List[str]] = Field(default=None, description="Optional tags/hashtags")


class PublishResponse(BaseModel):
    post_id: str
    url: Optional[HttpUrl] = None
    status: str = Field(default="published")
    published_at: str


class PublisherTool:
    name = "publisher"
    description = "Publish content to LinkedIn. Accepts text, optional media, visibility, and tags."

    def __init__(self, linkedin_api):
        """
        linkedin_api: an injected client providing an async `publish_post(...)` API.
        Expected signature:
            await linkedin_api.publish_post(
                user_id: str,
                content: str,
                media_urls: Optional[List[str]] = None,
                visibility: str = "connections",
                tags: Optional[List[str]] = None,
            ) -> Dict[str, Any]  # returns {'post_id': '...', 'url': '...'}
        """
        self.linkedin_api = linkedin_api

    async def run(self, **kwargs) -> Dict[str, Any]:
        req = PublishRequest(**kwargs)

        # Basic validation / normalization
        visibility = req.visibility.lower()
        if visibility not in {"public", "connections", "private"}:
            raise ValueError("visibility must be one of: public|connections|private")

        # Call the actual API client
        api_res: Dict[str, Any] = await self.linkedin_api.publish_post(
            user_id=req.user_id,
            content=req.content,
            media_urls=[str(u) for u in (req.media_urls or [])],
            visibility=visibility,
            tags=req.tags or [],
        )

        post_id = api_res.get("post_id") or None
        url = api_res.get("url") or None

        resp = PublishResponse(
            post_id=post_id,
            url=url,
            status="published" if post_id else "unknown",
            published_at=datetime.now(timezone.utc).isoformat(),
        )
        return resp.model_dump()