"""
Pydantic models for API request/response schemas
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class SourceType(str, Enum):
    RSS = "rss"
    YOUTUBE = "youtube"
    TWITTER = "twitter"

class ReactionType(str, Enum):
    THUMBS_UP = "👍"
    THUMBS_DOWN = "👎"

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseSchema):
    email: str
    name: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

# Source schemas
class SourceBase(BaseSchema):
    type: SourceType
    handle: str
    name: Optional[str] = None
    is_active: bool = True
    topic: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Topic/category of the source (e.g., technology, business, health)"
    )
    fetch_frequency: int = Field(
        default=3600,
        ge=300,  # Minimum 5 minutes (300 seconds)
        le=604800,  # Maximum 7 days (604800 seconds)
        description="How often to fetch content from this source (in seconds)"
    )

class SourceCreate(SourceBase):
    pass

class SourceUpdate(BaseSchema):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    topic: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Topic/category of the source"
    )
    fetch_frequency: Optional[int] = Field(
        default=None,
        ge=300,  # Minimum 5 minutes (300 seconds)
        le=604800,  # Maximum 7 days (604800 seconds)
        description="How often to fetch content from this source (in seconds)"
    )

class Source(SourceBase):
    id: str
    user_id: str
    last_fetched_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

# Item schemas
class ItemBase(BaseSchema):
    title: str
    url: HttpUrl
    summary: Optional[str] = None
    published_at: datetime
    source_id: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: str
    trend_score: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

# Style sample schemas
class StyleSampleBase(BaseSchema):
    content: str
    sample_type: str = "newsletter"  # newsletter, blog, social

class StyleSampleCreate(StyleSampleBase):
    pass

class StyleSample(StyleSampleBase):
    id: str
    user_id: str
    created_at: datetime

# Voice profile schemas
class VoiceProfile(BaseSchema):
    user_id: str
    traits: List[str]  # e.g., ["friendly", "analytical", "witty"]
    confidence: float
    created_at: datetime
    updated_at: datetime

# Draft schemas
class DraftBase(BaseSchema):
    title: str
    body_md: str
    status: str = "draft"  # draft, sent, published

class DraftCreate(DraftBase):
    pass

class Draft(DraftBase):
    id: str
    user_id: str
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

# Feedback schemas
class FeedbackBase(BaseSchema):
    draft_id: str
    reaction: ReactionType
    notes: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: str
    user_id: str
    created_at: datetime

# API Request/Response schemas
class IngestionRequest(BaseSchema):
    source_ids: List[str]
    force_refresh: bool = False

class IngestionResponse(BaseSchema):
    processed_sources: int
    new_items: int
    errors: List[str] = []

class TrendAnalysisRequest(BaseSchema):
    time_window_hours: int = 48
    limit: int = 20

class TrendAnalysisResponse(BaseSchema):
    trending_items: List[Item]
    analysis_metadata: Dict[str, Any]

class StyleTrainingRequest(BaseSchema):
    user_id: str
    samples: List[StyleSampleCreate]

class StyleTrainingResponse(BaseSchema):
    voice_profile: VoiceProfile
    confidence_score: float

class GenerationRequest(BaseSchema):
    trending_items: List[str] = []  # Item IDs (optional, will use trending if empty)
    custom_prompt: Optional[str] = None

class GenerationResponse(BaseSchema):
    draft: Draft
    generation_metadata: Dict[str, Any]

class DeliveryRequest(BaseSchema):
    draft_id: str
    send_immediately: bool = False

class DeliveryResponse(BaseSchema):
    success: bool
    delivery_id: Optional[str] = None
    error: Optional[str] = None
