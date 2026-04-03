"""
Analytics API Router
"""
from fastapi import APIRouter, Query
from typing import Optional

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.engines.analytics_engine import analytics_engine

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/dashboard")
async def get_dashboard():
    """Get comprehensive dashboard analytics."""
    try:
        result = analytics_engine.get_dashboard_analytics()
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/content")
async def get_content_analytics(
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    category: Optional[str] = Query(None, description="Filter by content category")
):
    """Get filtered content analytics."""
    try:
        result = analytics_engine.get_content_analytics(content_type, category)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/engagement")
async def get_engagement():
    """Get engagement metrics breakdown."""
    try:
        result = analytics_engine.get_dashboard_analytics()
        return {"status": "success", "data": {
            "engagement": result.get("engagement", {}),
            "peak_hours": result.get("peak_hours", {}),
            "ai_suggestions": result.get("ai_suggestions", [])
        }}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/growth")
async def get_growth():
    """Get growth trends and historical data."""
    try:
        result = analytics_engine.get_dashboard_analytics()
        return {"status": "success", "data": {
            "growth_trends": result.get("growth_trends", {}),
            "overview": result.get("overview", {})
        }}
    except Exception as e:
        return {"status": "error", "message": str(e)}
