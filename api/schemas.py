from pydantic import BaseModel, HttpUrl
from typing import Optional

class VideoRequest(BaseModel):
    url: HttpUrl  # Validates YouTube URL
    resolution: Optional[str] = None  # e.g., "720p", "1080p"
    # resolution: str = "720p"
    format: str = "mp4"  # Default format

class VideoMetadata(BaseModel):
    title: str
    author: str
    length: int  # in seconds
    views: int
    publish_date: str
    description: str