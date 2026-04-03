"""
🎯 AI Powered Viral Content & Digital Marketing Assistant
Main FastAPI Application Entry Point

Features:
- Real-time trend detection across Instagram, YouTube, Twitter
- Viral content prediction (ML-powered, 0-100 score)
- AI content generation (captions, hashtags, SEO)
- Platform-specific optimizers
- Comprehensive analytics dashboard
- AI Viral Coach chat assistant
- Auto content calendar generation
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, Body, UploadFile, File
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from backend.config import API_TITLE, API_VERSION, API_DESCRIPTION, CORS_ORIGINS
from backend.data.pipeline import pipeline
from backend.routers import trends, predict, content, analytics, optimizer, coach, media
from backend.engines.trend_engine import trend_engine
from backend.models.viral_predictor import viral_predictor
from backend.engines.content_engine import content_engine
from backend.engines.analytics_engine import analytics_engine
from backend.config import UPLOAD_DIR
import shutil

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    logger.info("🚀 Starting AI Viral Content Assistant...")
    
    # Initialize data pipeline
    try:
        result = pipeline.run()
        logger.info(f"📊 Data loaded: {result}")
    except Exception as e:
        logger.warning(f"⚠️ Data pipeline warning: {e}")
    
    # Train ML model if not already trained
    try:
        from backend.models.viral_predictor import viral_predictor
        if not viral_predictor.is_trained:
            metrics = viral_predictor.train()
            logger.info(f"🤖 Model trained: {metrics}")
        else:
            logger.info("🤖 Pre-trained model loaded")
    except Exception as e:
        logger.warning(f"⚠️ Model training warning: {e}")
    
    logger.info("✅ Application ready!")
    yield
    
    # Shutdown
    logger.info("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trends.router)
app.include_router(predict.router)
app.include_router(content.router)
app.include_router(analytics.router)
app.include_router(optimizer.router)
app.include_router(coach.router)
app.include_router(media.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error", "detail": str(exc)},
    )


@app.get("/")
async def root():
    """API Health Check & Info."""
    return {
        "name": API_TITLE,
        "version": API_VERSION,
        "status": "🟢 Online",
        "endpoints": {
            "docs": "/docs",
            "trends": "/api/trends/detect",
            "predict": "/api/predict/viral",
            "content": "/api/content/generate",
            "analytics": "/api/analytics/dashboard",
            "instagram": "/api/optimize/instagram",
            "youtube": "/api/optimize/youtube",
            "twitter": "/api/optimize/twitter",
            "coach": "/api/coach/chat",
            "calendar": "/api/coach/calendar",
            "strategy": "/api/coach/strategy",
            "alerts": "/api/coach/alerts"
            ,"upload_media": "/api/media/upload-media"
            ,"analyze_video": "/api/media/analyze-video"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": API_VERSION}


@app.get("/trend-detect")
async def trend_detect_alias(platform: str = "all"):
    return {"status": "success", "data": trend_engine.detect_trends(platform)}


@app.post("/predict-viral")
async def predict_viral_alias(payload: dict = Body(default={})):
    return {"status": "success", "data": viral_predictor.predict(payload)}


@app.post("/generate-content")
async def generate_content_alias(payload: dict = Body(default={})):
    topic = payload.get("topic", "AI marketing")
    platform = payload.get("platform", "instagram")
    tone = payload.get("tone", "casual")
    return {
        "status": "success",
        "data": content_engine.generate_content(
            topic=topic,
            platform=platform,
            tone=tone,
            content_type=payload.get("content_type"),
            target_audience=payload.get("target_audience"),
            niche=payload.get("niche"),
        ),
    }


@app.get("/analytics")
async def analytics_alias():
    return {"status": "success", "data": analytics_engine.get_dashboard_analytics()}


@app.post("/upload-media")
async def upload_media_alias(file: UploadFile = File(...)):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "status": "success",
        "data": {"filename": file.filename, "path": str(file_path), "size": file_path.stat().st_size},
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
