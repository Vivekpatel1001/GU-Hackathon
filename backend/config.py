"""
Configuration settings for the AI Viral Content Assistant backend.
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "backend" / "saved_models"
UPLOAD_DIR = BASE_DIR / "backend" / "uploads"
LOG_DIR = BASE_DIR / "backend" / "logs"
DB_PATH = BASE_DIR / "backend" / "app_data.db"

# Data file paths
INSTAGRAM_CSV = DATA_DIR / "Instagram_Analytics.csv"
YOUTUBE_CSV = DATA_DIR / "youtube_trending_data.csv"
TWITTER_CSV = DATA_DIR / "training.1600000.processed.noemoticon (1).csv"

# Model paths
VIRAL_MODEL_PATH = MODEL_DIR / "viral_model.pkl"
SCALER_PATH = MODEL_DIR / "scaler.pkl"
SENTIMENT_MODEL_PATH = MODEL_DIR / "sentiment_model.pkl"
TFIDF_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"

# API Settings
API_TITLE = "AI Viral Content & Digital Marketing Assistant"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Production-ready AI system for viral content prediction, trend detection, and content optimization"

# CORS Settings
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "*"
]

# Content Generation Templates
PLATFORM_CONFIGS = {
    "instagram": {
        "max_hashtags": 30,
        "optimal_caption_length": (125, 2200),
        "content_types": ["Reel", "Story", "Carousel", "Photo", "Video"],
        "peak_hours": [9, 11, 12, 14, 17, 19, 21],
    },
    "youtube": {
        "max_tags": 500,
        "optimal_title_length": (60, 70),
        "optimal_description_length": (200, 5000),
        "peak_hours": [12, 14, 15, 16, 17],
    },
    "twitter": {
        "max_characters": 280,
        "optimal_hashtags": (1, 3),
        "peak_hours": [9, 12, 15, 17, 18, 21],
        "tweet_types": ["single", "thread", "question"],
    }
}

# Niches/Categories
CONTENT_CATEGORIES = [
    "Technology", "Fashion", "Beauty", "Food", "Travel",
    "Fitness", "Music", "Comedy", "Photography", "Lifestyle"
]

TONES = ["professional", "casual", "viral", "humorous", "inspirational"]

# Data Pipeline Runtime
PIPELINE_TWITTER_ROWS = int(os.getenv("PIPELINE_TWITTER_ROWS", "50000"))
PIPELINE_FETCH_TIMEOUT = int(os.getenv("PIPELINE_FETCH_TIMEOUT", "20"))

# External adapters (optional for real-time mode)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
