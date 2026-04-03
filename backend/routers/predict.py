"""
Viral Prediction API Router
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.models.viral_predictor import viral_predictor

router = APIRouter(prefix="/api/predict", tags=["Viral Prediction"])


class PredictionRequest(BaseModel):
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    reach: int = 1000
    impressions: int = 1500
    caption_length: int = 200
    hashtags_count: int = 10
    followers_gained: int = 50
    upload_hour: int = 12
    upload_month: int = 1
    media_type: str = "Reel"
    content_category: str = "Technology"
    traffic_source: str = "Explore"


@router.post("/viral")
async def predict_viral(request: PredictionRequest):
    """Predict virality score (0-100) for content."""
    try:
        features = request.model_dump()
        
        # Calculate derived features
        features['total_engagement'] = features['likes'] + features['comments'] + features['shares'] + features['saves']
        features['engagement_per_reach'] = features['total_engagement'] / max(features['reach'], 1) * 100
        features['save_rate'] = features['saves'] / max(features['reach'], 1) * 100
        features['comment_to_like_ratio'] = features['comments'] / max(features['likes'], 1)
        features['is_weekend'] = 1 if features.get('upload_day', '') in ['Saturday', 'Sunday'] else 0
        
        result = viral_predictor.predict(features)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/train")
async def train_model():
    """Train/retrain the viral prediction model."""
    try:
        metrics = viral_predictor.train()
        return {"status": "success", "data": {"message": "Model trained successfully!", "metrics": metrics}}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/refresh")
async def refresh_prediction():
    """Refresh prediction model with latest data."""
    try:
        metrics = viral_predictor.train()
        return {"status": "success", "data": {"message": "Model refreshed!", "metrics": metrics}}
    except Exception as e:
        return {"status": "error", "message": str(e)}
