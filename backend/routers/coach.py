"""
AI Viral Coach - Chat assistant for content strategy and marketing advice.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import random

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.engines.trend_engine import trend_engine
from backend.engines.content_engine import content_engine
from backend.engines.analytics_engine import analytics_engine

router = APIRouter(prefix="/api/coach", tags=["AI Viral Coach"])


class ChatMessage(BaseModel):
    message: str
    context: Optional[str] = None


class CalendarRequest(BaseModel):
    topic: str
    platform: str = "all"
    days: int = 7


@router.post("/chat")
async def chat_with_coach(request: ChatMessage):
    """Chat with AI Viral Coach for content advice."""
    try:
        message = request.message.lower()
        response = _generate_coach_response(message, request.context)
        return {"status": "success", "data": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/calendar")
async def generate_content_calendar(request: CalendarRequest):
    """Generate an auto content calendar."""
    try:
        calendar = _generate_calendar(request.topic, request.platform, request.days)
        return {"status": "success", "data": calendar}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/strategy")
async def get_cross_platform_strategy():
    """Get cross-platform content strategy recommendations."""
    try:
        trends = trend_engine.detect_trends("all")
        analytics = analytics_engine.get_dashboard_analytics()
        
        strategy = {
            "overview": "Cross-Platform Digital Marketing Strategy 2026",
            "platforms": {
                "instagram": {
                    "focus": "Visual storytelling & short-form video",
                    "frequency": "4-5 posts/week + daily stories",
                    "content_mix": "60% Reels, 20% Carousels, 10% Photos, 10% Stories",
                    "growth_tactics": [
                        "Use trending audio in Reels",
                        "Create saveable/shareable carousel content",
                        "Collaborate with micro-influencers",
                        "Use Instagram SEO (keywords in captions & alt text)"
                    ]
                },
                "youtube": {
                    "focus": "Long-form educational & entertainment content",
                    "frequency": "2 videos/week + 3-4 Shorts/week",
                    "content_mix": "50% tutorials, 30% vlogs/entertainment, 20% shorts",
                    "growth_tactics": [
                        "Optimize titles & thumbnails for CTR",
                        "Use YouTube SEO (tags, description, chapters)",
                        "Create playlists for watch time",
                        "End screens & cards for funnel"
                    ]
                },
                "twitter": {
                    "focus": "Thought leadership & community building",
                    "frequency": "3-5 tweets/day + 1-2 threads/week",
                    "content_mix": "40% insights, 30% engagement, 20% threads, 10% polls",
                    "growth_tactics": [
                        "Engage in trending conversations",
                        "Create viral threads",
                        "Use strategic quote tweets",
                        "Build a consistent brand voice"
                    ]
                }
            },
            "trending_topics": trends.get("trending_topics", [])[:5],
            "ai_suggestions": analytics.get("ai_suggestions", [])[:5],
            "key_metrics_to_track": [
                "Engagement Rate (target: >5%)",
                "Follower Growth Rate (target: >2%/week)",
                "Content Reach (target: growing each month)",
                "Save/Share Rate (target: >3%)",
                "Conversion Rate (clicks, leads, sales)"
            ]
        }
        
        return {"status": "success", "data": strategy}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/alerts")
async def get_trend_alerts():
    """Get real-time trend alerts."""
    try:
        trends = trend_engine.detect_trends("all")
        
        alerts = []
        # Check for trending topics
        topics = trends.get("trending_topics", [])
        for topic in topics[:5]:
            alerts.append({
                "type": "trend",
                "priority": "high",
                "message": f"📈 '{topic.get('topic', '')}' is trending on {topic.get('platform', '')}!",
                "action": f"Create content about this topic now for maximum reach",
                "platform": topic.get("platform", "")
            })
        
        # Check for hashtag spikes
        hashtags = trends.get("trending_hashtags", [])
        for ht in hashtags[:3]:
            alerts.append({
                "type": "hashtag",
                "priority": "medium",
                "message": f"#️⃣ {ht.get('hashtag', '')} is gaining traction!",
                "action": "Use this hashtag in your next post",
                "platform": ht.get("platform", "")
            })
        
        return {"status": "success", "data": {"alerts": alerts, "count": len(alerts)}}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def _generate_coach_response(message: str, context: str = None) -> dict:
    """Generate contextual coaching response."""
    
    # Intent detection
    if any(w in message for w in ["trend", "trending", "viral", "popular"]):
        trends = trend_engine.detect_trends("all")
        topics = trends.get("trending_topics", [])[:5]
        return {
            "response": "🔥 Here are the current trending topics across platforms!",
            "data": topics,
            "suggestions": [
                "Create content around these topics within 24 hours",
                "Use trending hashtags in your posts",
                "Monitor these trends for the next 48 hours"
            ]
        }
    
    elif any(w in message for w in ["hashtag", "tag", "#"]):
        return {
            "response": "📌 Here are my hashtag recommendations:",
            "suggestions": [
                "Use 10-15 hashtags on Instagram (mix of popular and niche)",
                "Use 1-3 hashtags on Twitter for best engagement",
                "Research hashtag volume before using them",
                "Create a branded hashtag for your content",
                "Rotate hashtags to avoid shadowban"
            ]
        }
    
    elif any(w in message for w in ["best time", "when", "schedule", "posting time"]):
        return {
            "response": "⏰ Optimal posting times based on our data analysis:",
            "data": {
                "instagram": "9 AM, 12 PM, 7 PM (your audience's timezone)",
                "youtube": "2 PM - 4 PM on weekdays",
                "twitter": "9 AM, 12 PM, 5 PM"
            },
            "suggestions": [
                "Test different times and track results",
                "Use scheduling tools for consistency",
                "Weekdays generally outperform weekends"
            ]
        }
    
    elif any(w in message for w in ["grow", "growth", "followers", "audience"]):
        return {
            "response": "📈 Here's your growth strategy roadmap:",
            "suggestions": [
                "1. Post consistently (at least 4x/week)",
                "2. Engage with your audience (reply to every comment)",
                "3. Collaborate with creators in your niche",
                "4. Use cross-platform promotion",
                "5. Create shareable content (educational or entertaining)",
                "6. Run giveaways or challenges",
                "7. Optimize your bio and profile",
                "8. Use stories/reels for algorithm boost"
            ]
        }
    
    elif any(w in message for w in ["caption", "write", "text", "copy"]):
        return {
            "response": "✍️ Caption writing tips for maximum engagement:",
            "suggestions": [
                "Start with a hook (question, bold statement, or story)",
                "Use line breaks for readability",
                "Include a clear CTA (Call to Action)",
                "Add relevant emojis for visual appeal",
                "Keep it authentic to your brand voice",
                "Instagram: 125-2200 chars | Twitter: under 280 chars"
            ]
        }
    
    else:
        return {
            "response": f"🤖 Great question! Here's my advice on '{message}':",
            "suggestions": [
                "Focus on creating value-driven content",
                "Consistency is key - post regularly",
                "Engage authentically with your community",
                "Track your metrics and iterate",
                "Stay updated with platform algorithm changes",
                "Experiment with different content formats"
            ],
            "tip": "💡 Pro tip: Ask me about trends, hashtags, posting times, growth strategies, or caption writing!"
        }


def _generate_calendar(topic: str, platform: str, days: int) -> dict:
    """Generate a content calendar."""
    content_types = {
        "instagram": ["Reel", "Carousel", "Photo", "Story", "Video"],
        "youtube": ["Tutorial", "Vlog", "Short", "Review", "Live"],
        "twitter": ["Thread", "Single", "Poll", "Question", "Quote"],
    }
    
    tones = ["viral", "professional", "casual", "humorous", "inspirational"]
    
    calendar = []
    for day in range(1, days + 1):
        day_plan = {"day": day}
        
        if platform == "all":
            platforms = ["instagram", "youtube", "twitter"]
        else:
            platforms = [platform]
        
        for p in platforms:
            types = content_types.get(p, ["Post"])
            ct = types[(day - 1) % len(types)]
            tone = tones[(day - 1) % len(tones)]
            
            content = content_engine.generate_content(
                topic=topic, platform=p, tone=tone, content_type=ct
            )
            
            day_plan[p] = {
                "content_type": ct,
                "tone": tone,
                "hook": content.get("hook", ""),
                "caption_preview": (content.get("caption", content.get("tweet", ""))[:100] + "...") if content.get("caption", content.get("tweet", "")) else "",
                "time": content.get("best_posting_time", "12:00")
            }
        
        calendar.append(day_plan)
    
    return {
        "topic": topic,
        "duration_days": days,
        "calendar": calendar,
        "tips": [
            "Batch create content on weekends for the week ahead",
            "Mix content types to keep your feed diverse",
            "Repurpose top-performing content across platforms",
            "Leave room for real-time trend-jacking"
        ]
    }
