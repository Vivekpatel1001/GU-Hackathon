"""
Trend Detection Engine - Identifies trending hashtags, keywords, and topics
using frequency analysis, TF-IDF, and time-based spike detection.
"""
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import logging
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from backend.data.pipeline import pipeline

logger = logging.getLogger(__name__)


class TrendEngine:
    """Detects trending topics, hashtags, and keywords across platforms."""
    
    def __init__(self):
        self.tfidf = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1, 2))
    
    def detect_trends(self, platform: str = "all") -> dict:
        """Detect trending topics across platforms."""
        results = {
            "trending_hashtags": [],
            "trending_keywords": [],
            "trending_topics": [],
            "spike_detected": [],
            "related_hashtag_suggestions": [],
            "platform_breakdown": {}
        }
        
        if platform in ("all", "instagram"):
            ig_trends = self._analyze_instagram_trends()
            results["platform_breakdown"]["instagram"] = ig_trends
        
        if platform in ("all", "youtube"):
            yt_trends = self._analyze_youtube_trends()
            results["platform_breakdown"]["youtube"] = yt_trends
        
        if platform in ("all", "twitter"):
            tw_trends = self._analyze_twitter_trends()
            results["platform_breakdown"]["twitter"] = tw_trends
        
        # Aggregate top trends
        results["trending_hashtags"] = self._aggregate_hashtags(results["platform_breakdown"])
        results["trending_keywords"] = self._aggregate_keywords(results["platform_breakdown"])
        results["trending_topics"] = self._aggregate_topics(results["platform_breakdown"])
        results["spike_detected"] = self._detect_time_spikes(results["platform_breakdown"])
        results["related_hashtag_suggestions"] = self._related_hashtags(results["trending_keywords"])
        
        return results

    def _detect_time_spikes(self, breakdown: dict) -> list:
        spikes = []

        ig = breakdown.get("instagram", {})
        for point in ig.get("peak_hours", [])[:5]:
            if point.get("avg_engagement", 0) >= 8:
                spikes.append(
                    {
                        "platform": "instagram",
                        "time_bucket": f"{point.get('hour', 0)}:00",
                        "signal": "engagement_spike",
                        "score": point.get("avg_engagement", 0),
                    }
                )

        yt = breakdown.get("youtube", {})
        for point in yt.get("peak_hours", [])[:5]:
            if point.get("avg_views", 0) >= 10000:
                spikes.append(
                    {
                        "platform": "youtube",
                        "time_bucket": f"{point.get('hour', 0)}:00",
                        "signal": "view_spike",
                        "score": point.get("avg_views", 0),
                    }
                )

        tw = breakdown.get("twitter", {})
        for ht in tw.get("trending_hashtags", [])[:5]:
            if ht.get("count", 0) >= 20:
                spikes.append(
                    {
                        "platform": "twitter",
                        "time_bucket": "realtime",
                        "signal": "hashtag_spike",
                        "score": ht.get("count", 0),
                        "topic": ht.get("hashtag", ""),
                    }
                )

        return spikes[:10]

    def _related_hashtags(self, keywords: list) -> list:
        suggestions = []
        seen = set()
        for item in keywords[:10]:
            keyword = str(item.get("keyword", "")).strip().lower().replace(" ", "")
            if not keyword:
                continue
            for suffix in ("tips", "today", "creator", "growth"):
                candidate = f"#{keyword}{suffix}"
                if candidate not in seen:
                    seen.add(candidate)
                    suggestions.append(candidate)
        return suggestions[:20]
    
    def _analyze_instagram_trends(self) -> dict:
        """Analyze Instagram trends from analytics data."""
        df = pipeline.get_instagram_data()
        if df.empty:
            return {"hashtags": [], "categories": [], "peak_times": []}
        
        # Top performing categories by engagement
        category_engagement = df.groupby('content_category').agg({
            'engagement_rate': 'mean',
            'likes': 'sum',
            'shares': 'sum',
            'post_id': 'count'
        }).rename(columns={'post_id': 'post_count'})
        category_engagement = category_engagement.sort_values('engagement_rate', ascending=False)
        
        top_categories = []
        for cat, row in category_engagement.head(10).iterrows():
            top_categories.append({
                "category": cat,
                "avg_engagement_rate": round(row['engagement_rate'], 2),
                "total_likes": int(row['likes']),
                "post_count": int(row['post_count'])
            })
        
        # Best performing content types
        type_perf = df.groupby('media_type').agg({
            'engagement_rate': 'mean',
            'likes': 'mean',
            'shares': 'mean'
        }).sort_values('engagement_rate', ascending=False)
        
        content_types = []
        for ct, row in type_perf.iterrows():
            content_types.append({
                "type": ct,
                "avg_engagement": round(row['engagement_rate'], 2),
                "avg_likes": int(row['likes']),
                "avg_shares": int(row['shares'])
            })
        
        # Peak posting hours
        if 'upload_hour' in df.columns:
            hour_engagement = df.groupby('upload_hour')['engagement_rate'].mean().sort_values(ascending=False)
            peak_hours = [{"hour": int(h), "avg_engagement": round(e, 2)} for h, e in hour_engagement.head(5).items()]
        else:
            peak_hours = []
        
        # Traffic sources
        source_perf = df.groupby('traffic_source').agg({
            'engagement_rate': 'mean',
            'reach': 'sum'
        }).sort_values('reach', ascending=False)
        
        traffic = []
        for src, row in source_perf.iterrows():
            traffic.append({
                "source": src,
                "avg_engagement": round(row['engagement_rate'], 2),
                "total_reach": int(row['reach'])
            })
        
        return {
            "top_categories": top_categories,
            "content_types": content_types,
            "peak_hours": peak_hours,
            "traffic_sources": traffic,
            "total_posts_analyzed": len(df)
        }
    
    def _analyze_youtube_trends(self) -> dict:
        """Analyze YouTube trends from trending data."""
        df = pipeline.get_youtube_data()
        if df.empty:
            return {"trending_videos": [], "keywords": []}
        
        # Top trending videos by engagement
        if 'Engagement_Score' in df.columns:
            score_col = 'Engagement_Score'
        elif 'Like_Rate' in df.columns:
            score_col = 'Like_Rate'
        else:
            df['_score'] = df.get('Likes', 0) / df.get('Views', 1).replace(0, 1) * 100
            score_col = '_score'
        
        top_videos = df.nlargest(10, score_col)
        trending_videos = []
        for _, row in top_videos.iterrows():
            trending_videos.append({
                "title": str(row.get('Title', '')),
                "channel": str(row.get('Channel', '')),
                "views": int(row.get('Views', 0)),
                "likes": int(row.get('Likes', 0)),
                "engagement_score": round(float(row.get(score_col, 0)), 2)
            })
        
        # Extract keywords from titles using TF-IDF
        titles = df['Title'].dropna().tolist() if 'Title' in df.columns else []
        if titles:
            try:
                tfidf_matrix = self.tfidf.fit_transform(titles)
                feature_names = self.tfidf.get_feature_names_out()
                avg_scores = tfidf_matrix.mean(axis=0).A1
                top_indices = avg_scores.argsort()[-20:][::-1]
                keywords = [{"keyword": feature_names[i], "score": round(avg_scores[i], 4)} for i in top_indices]
            except Exception:
                keywords = []
        else:
            keywords = []
        
        # Peak posting hours
        if 'Posting_Hour' in df.columns:
            hour_views = df.groupby('Posting_Hour')['Views'].mean().sort_values(ascending=False)
            peak_hours = [{"hour": int(h), "avg_views": int(v)} for h, v in hour_views.head(5).items()]
        else:
            peak_hours = []
        
        # Channel performance
        channel_perf = df.groupby('Channel').agg({
            'Views': 'sum',
            'Likes': 'sum'
        }).sort_values('Views', ascending=False).head(10)
        
        top_channels = [{"channel": ch, "total_views": int(row['Views']), "total_likes": int(row['Likes'])} 
                       for ch, row in channel_perf.iterrows()]
        
        return {
            "trending_videos": trending_videos,
            "keywords": keywords,
            "peak_hours": peak_hours,
            "top_channels": top_channels,
            "total_videos_analyzed": len(df)
        }
    
    def _analyze_twitter_trends(self) -> dict:
        """Analyze Twitter trends from sentiment data."""
        df = pipeline.get_twitter_data()
        if df.empty:
            return {"hashtags": [], "sentiment": {}}
        
        # Extract hashtags
        texts = df['text'].dropna().tolist() if 'text' in df.columns else []
        hashtags = []
        for text in texts:
            tags = re.findall(r'#(\w+)', str(text))
            hashtags.extend([t.lower() for t in tags])
        
        hashtag_counts = Counter(hashtags).most_common(20)
        trending_hashtags = [{"hashtag": f"#{h}", "count": c} for h, c in hashtag_counts]
        
        # Sentiment distribution
        sentiment_dist = {}
        if 'sentiment_label' in df.columns:
            dist = df['sentiment_label'].value_counts()
            sentiment_dist = {str(k): int(v) for k, v in dist.items()}
        
        # Top mentioned users
        mentions = []
        for text in texts:
            users = re.findall(r'@(\w+)', str(text))
            mentions.extend([u.lower() for u in users])
        mention_counts = Counter(mentions).most_common(10)
        top_mentions = [{"user": f"@{u}", "count": c} for u, c in mention_counts]
        
        # Word frequency (keywords)
        all_words = []
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'it', 'this', 'that', 'and', 'or', 'but', 'not', 'be', 'have', 'has', 'had', 'do', 'did', 'will', 'would', 'can', 'could', 'i', 'you', 'he', 'she', 'we', 'they', 'my', 'your', 'his', 'her', 'our', 'their', 'me', 'him', 'us', 'them', 'so', 'if', 'just', 'im', 'dont', 'its'}
        for text in texts[:5000]:
            words = re.findall(r'\b[a-z]{3,}\b', str(text).lower())
            all_words.extend([w for w in words if w not in stop_words])
        
        word_counts = Counter(all_words).most_common(15)
        trending_words = [{"word": w, "count": c} for w, c in word_counts]
        
        return {
            "trending_hashtags": trending_hashtags,
            "sentiment_distribution": sentiment_dist,
            "top_mentions": top_mentions,
            "trending_words": trending_words,
            "total_tweets_analyzed": len(df)
        }
    
    def _aggregate_hashtags(self, breakdown: dict) -> list:
        all_hashtags = []
        for platform, data in breakdown.items():
            if 'trending_hashtags' in data:
                for h in data['trending_hashtags']:
                    all_hashtags.append({**h, "platform": platform})
        return sorted(all_hashtags, key=lambda x: x.get('count', 0), reverse=True)[:15]
    
    def _aggregate_keywords(self, breakdown: dict) -> list:
        all_keywords = []
        for platform, data in breakdown.items():
            if 'keywords' in data:
                for k in data['keywords']:
                    all_keywords.append({**k, "platform": platform})
            if 'trending_words' in data:
                for w in data['trending_words']:
                    all_keywords.append({"keyword": w['word'], "score": w['count'], "platform": platform})
        return sorted(all_keywords, key=lambda x: x.get('score', 0), reverse=True)[:15]
    
    def _aggregate_topics(self, breakdown: dict) -> list:
        topics = []
        if 'instagram' in breakdown and 'top_categories' in breakdown['instagram']:
            for cat in breakdown['instagram']['top_categories'][:5]:
                topics.append({
                    "topic": cat['category'],
                    "engagement": cat['avg_engagement_rate'],
                    "platform": "instagram"
                })
        if 'youtube' in breakdown and 'trending_videos' in breakdown['youtube']:
            for vid in breakdown['youtube']['trending_videos'][:5]:
                topics.append({
                    "topic": vid['title'][:50],
                    "engagement": vid['engagement_score'],
                    "platform": "youtube"
                })
        return topics
    
    def search_hashtags(self, query: str) -> dict:
        """Search for hashtag suggestions based on a query."""
        df_ig = pipeline.get_instagram_data()
        df_yt = pipeline.get_youtube_data()
        
        suggestions = []
        related_categories = []
        
        # Find related content from Instagram
        if not df_ig.empty and 'content_category' in df_ig.columns:
            matching = df_ig[df_ig['content_category'].str.lower().str.contains(query.lower(), na=False)]
            if not matching.empty:
                avg_eng = matching['engagement_rate'].mean()
                suggestions.append({
                    "hashtag": f"#{query}",
                    "estimated_reach": int(matching['reach'].mean()),
                    "avg_engagement": round(avg_eng, 2)
                })
                # Related categories
                related = df_ig['content_category'].value_counts().head(5)
                related_categories = [{"category": cat, "posts": int(cnt)} for cat, cnt in related.items()]
        
        # Generate related hashtags
        related_hashtags = [
            f"#{query}tips", f"#{query}daily", f"#{query}life",
            f"#{query}lover", f"#{query}community", f"#{query}content",
            f"#{query}creator", f"#{query}vibes", f"#{query}goals",
            f"#trending{query}"
        ]
        
        return {
            "query": query,
            "suggestions": suggestions,
            "related_hashtags": related_hashtags,
            "related_categories": related_categories
        }


# Global instance
trend_engine = TrendEngine()
