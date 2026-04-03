# AI Powered Viral Content and Digital Marketing Assistant

Production-ready, modular system for trend intelligence, virality prediction, content optimization, and cross-platform analytics.

## What is implemented
- End-to-end FastAPI backend with modular routers and engines.
- Data pipeline using your three CSV datasets with cleaning, feature prep, CSV exports, and SQLite persistence.
- Trend detection engine with hashtag/keyword/topic extraction, related hashtag suggestions, and spike signals.
- Viral score prediction model with train/retrain/refresh support and saved model artifacts.
- NLP content engine for captions, hooks, hashtags, SEO tags, and platform tone adaptation.
- Analytics engine with overview, graph-ready data, peak hours, and today-vs-previous comparison.
- AI Viral Coach endpoints for chat, strategy, trend alerts, and content calendar generation.
- Frame-level video analysis with attention-drop detection and recommendations.
- Next.js frontend pages wired to backend APIs for dashboard, optimizers, trends, analytics, and generator.
- Six notebooks covering collection, cleaning, trend detection, feature engineering, training, and evaluation.

## Architecture
- Backend: FastAPI + modular engines in backend/engines
- ML/NLP: scikit-learn + TF-IDF + feature engineering in backend/models
- Data: pandas + SQLite in backend/data and backend/app_data.db
- Frontend: Next.js app router + reusable UI components
- Notebooks: documented ML lifecycle in notebooks

## One-command data pipeline
Run from project root:

```bash
python -m backend.data.pipeline
```

This command:
- Loads Instagram, YouTube, and Twitter datasets
- Cleans and normalizes text and numeric columns
- Writes cleaned CSVs to data/cleaned
- Persists cleaned tables to SQLite at backend/app_data.db

## Setup and run

1. Backend setup

```bash
cd backend
pip install -r requirements.txt
cd ..
```

2. Start API server

```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

4. Open
- API docs: http://127.0.0.1:8000/docs
- Frontend: http://127.0.0.1:3000

Optional frontend env:

```bash
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Key API endpoints

Primary grouped APIs:
- GET /api/trends/detect
- GET /api/trends/realtime
- POST /api/predict/viral
- POST /api/content/generate
- GET /api/analytics/dashboard
- POST /api/optimize/instagram
- POST /api/optimize/youtube
- POST /api/optimize/twitter
- POST /api/media/upload-media
- POST /api/media/analyze-video

Prompt-compatible alias APIs:
- GET /trend-detect
- POST /predict-viral
- POST /generate-content
- GET /analytics
- POST /upload-media

## Notebook list
- notebooks/01_data_collection.ipynb
- notebooks/02_data_cleaning.ipynb
- notebooks/03_trend_detection.ipynb
- notebooks/04_feature_engineering.ipynb
- notebooks/05_model_training.ipynb
- notebooks/06_evaluation.ipynb

## Hackathon standout ideas
- Real-time stream mode with Kafka producer + Flink consumer for trend velocity scoring.
- Attention drop heatmap overlay on timeline for creator editing workflow.
- Cross-platform repurposing assistant that converts one source content into Insta Reel script, YouTube outline, and X thread.
- Auto content calendar with risk/opportunity scores per slot.
- “What-if” simulator for virality score by changing hashtags, posting hour, and hook style.

## Demo presentation flow
1. Problem: creators lack data-driven cross-platform optimization.
2. Live data pipeline run in one command.
3. Real-time trend + spike dashboard.
4. Viral prediction and refresh model action.
5. Instagram/YouTube/Twitter optimizer outputs.
6. Video frame analysis showing attention drop timestamps.
7. Business value: increased engagement, lower content iteration time.

## Notes
- For full frame-level video analysis, ensure OpenCV dependency installs successfully.
- API credentials for real-time external sources can be added via environment variables in backend/config.py.
