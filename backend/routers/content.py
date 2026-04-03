"""
Content Generation API Router
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.engines.content_engine import content_engine

router = APIRouter(prefix="/api/content", tags=["Content Generation"])


class ContentRequest(BaseModel):
    topic: str
    platform: str = "instagram"
    tone: str = "casual"
    content_type: Optional[str] = None
    target_audience: Optional[str] = None
    niche: Optional[str] = None


class IdeaRequest(BaseModel):
    topic: str
    platform: str = "all"
    tone: str = "casual"
    target_audience: Optional[str] = None


@router.post("/generate")
async def generate_content(request: ContentRequest):
    """Generate optimized content for any platform."""
    try:
        result = content_engine.generate_content(
            topic=request.topic,
            platform=request.platform,
            tone=request.tone,
            content_type=request.content_type,
            target_audience=request.target_audience,
            niche=request.niche
        )
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/ideas")
async def generate_ideas(request: IdeaRequest):
    """Generate multi-platform content ideas."""
    try:
        result = content_engine.generate_ideas(
            topic=request.topic,
            platform=request.platform,
            tone=request.tone,
            target_audience=request.target_audience
        )
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
