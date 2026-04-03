"""
Trend Detection API Router
"""
from fastapi import APIRouter, Query
from typing import Optional

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.engines.trend_engine import trend_engine

router = APIRouter(prefix="/api/trends", tags=["Trend Detection"])


@router.get("/detect")
async def detect_trends(platform: Optional[str] = Query("all", description="Platform: all, instagram, youtube, twitter")):
    """Detect trending topics, hashtags, and keywords."""
    try:
        results = trend_engine.detect_trends(platform)
        return {"status": "success", "data": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/hashtags/search")
async def search_hashtags(q: str = Query(..., description="Hashtag search query")):
    """Search for hashtag suggestions."""
    try:
        results = trend_engine.search_hashtags(q)
        return {"status": "success", "data": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/realtime")
async def get_realtime_trends():
    """Get real-time trending data across all platforms."""
    try:
        results = trend_engine.detect_trends("all")
        return {
            "status": "success",
            "data": {
                "trending_now": results.get("trending_topics", [])[:10],
                "hot_hashtags": results.get("trending_hashtags", [])[:10],
                "top_keywords": results.get("trending_keywords", [])[:10],
                "timestamp": "real-time"
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
