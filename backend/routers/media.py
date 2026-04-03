"""Media router for upload and frame-level video analytics."""

from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.config import UPLOAD_DIR
from backend.engines.video_engine import video_engine

router = APIRouter(prefix="/api/media", tags=["Media Analysis"])


@router.post("/upload-media")
async def upload_media(file: UploadFile = File(...)):
    """Upload media file to local storage."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "data": {
            "filename": file.filename,
            "path": str(file_path),
            "size": file_path.stat().st_size,
        },
    }


@router.post("/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    """Upload and analyze a video frame-by-frame."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    analysis = video_engine.analyze_video(str(file_path))
    return {"status": "success", "data": analysis}


@router.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """Upload and analyze an image for Instagram-style quality feedback."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    analysis = video_engine.analyze_image(str(file_path))
    return {"status": "success", "data": analysis}


@router.post("/analyze-thumbnail")
async def analyze_thumbnail(file: UploadFile = File(...)):
    """Upload and score a YouTube thumbnail with change recommendations."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    analysis = video_engine.analyze_thumbnail(str(file_path))
    return {"status": "success", "data": analysis}
