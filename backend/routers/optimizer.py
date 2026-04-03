"""
Platform Optimizer API Router - Instagram, YouTube, Twitter/X optimizers
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.engines.content_engine import content_engine
from backend.engines.analytics_engine import analytics_engine

router = APIRouter(prefix="/api/optimize", tags=["Platform Optimizers"])


# ======================== INSTAGRAM ========================

class InstagramOptimizeRequest(BaseModel):
    content_type: str = "Reel"  # Reel, Story, Carousel, Photo, Video
    niche: str = "Technology"
    description: Optional[str] = None
    topic: Optional[str] = None


@router.post("/instagram")
async def optimize_instagram(request: InstagramOptimizeRequest):
    """Optimize content for Instagram."""
    try:
        topic = request.topic or request.niche
        content = content_engine.generate_content(
            topic=topic,
            platform="instagram",
            tone="viral",
            content_type=request.content_type,
            niche=request.niche
        )
        
        # Get platform-specific analytics
        analytics = analytics_engine.get_content_analytics(
            content_type=request.content_type,
            category=request.niche
        )
        
        return {
            "status": "success",
            "data": {
                "best_posting_time": content.get("best_posting_time", "9:00 AM"),
                "hashtags": content.get("hashtags", ""),
                "caption": content.get("caption", ""),
                "hook": content.get("hook", ""),
                "improvements": content.get("improvements", []),
                "seo_keywords": content.get("seo_keywords", []),
                "content_type": request.content_type,
                "niche": request.niche,
                "analytics_insight": analytics.get("suggestions", [])[:3]
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ======================== YOUTUBE ========================

class YouTubeOptimizeRequest(BaseModel):
    video_description: str = ""
    category: str = "Technology"
    duration: Optional[str] = "10:00"
    topic: Optional[str] = None


@router.post("/youtube")
async def optimize_youtube(request: YouTubeOptimizeRequest):
    """Optimize content for YouTube."""
    try:
        topic = request.topic or request.category
        content = content_engine.generate_content(
            topic=topic,
            platform="youtube",
            tone="professional"
        )
        
        return {
            "status": "success",
            "data": {
                "seo_title": content.get("title", ""),
                "seo_description": content.get("description", ""),
                "tags": content.get("tags", []),
                "thumbnail_suggestion": content.get("thumbnail_suggestion", ""),
                "engagement_tips": content.get("engagement_tips", []),
                "category": request.category,
                "optimal_duration": "8-12 minutes for maximum watch time",
                "upload_schedule": "Tuesdays and Thursdays at 2 PM yield highest views"
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ======================== TWITTER/X ========================

class TwitterOptimizeRequest(BaseModel):
    tweet_idea: str = ""
    tone: str = "casual"
    tweet_type: str = "single"  # single, thread, question
    topic: Optional[str] = None


@router.post("/twitter")
async def optimize_twitter(request: TwitterOptimizeRequest):
    """Optimize content for Twitter/X."""
    try:
        topic = request.topic or request.tweet_idea[:50]
        content = content_engine.generate_content(
            topic=topic,
            platform="twitter",
            tone=request.tone,
            content_type=request.tweet_type
        )
        
        return {
            "status": "success",
            "data": {
                "optimized_tweet": content.get("tweet", ""),
                "improved_wording": content.get("improved_tweet", ""),
                "thread": content.get("thread"),
                "character_count": content.get("character_count", 0),
                "engagement_suggestions": content.get("engagement_suggestions", []),
                "tone": request.tone,
                "tweet_type": request.tweet_type,
                "best_times": ["9:00 AM", "12:00 PM", "5:00 PM", "9:00 PM"]
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
