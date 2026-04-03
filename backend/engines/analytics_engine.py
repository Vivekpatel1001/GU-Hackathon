"""
Analytics Engine - Comprehensive engagement analytics, growth trends,
and AI-powered insights from real data.
"""
import pandas as pd
import numpy as np
import logging
from pathlib import Path
import sys
from datetime import datetime, timedelta

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from backend.data.pipeline import pipeline

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """Analytics engine providing engagement metrics, growth trends, and insights."""
    
    def get_dashboard_analytics(self) -> dict:
        """Get comprehensive dashboard analytics."""
        ig_data = pipeline.get_instagram_data()
        yt_data = pipeline.get_youtube_data()
        
        return {
            "overview": self._get_overview(ig_data, yt_data),
            "engagement": self._get_engagement_metrics(ig_data),
            "growth_trends": self._get_growth_trends(ig_data),
            "today_vs_previous": self._today_vs_previous(ig_data),
            "graph_data": self._graph_ready_series(ig_data),
            "peak_hours": self._get_peak_hours(ig_data, yt_data),
            "platform_comparison": self._get_platform_comparison(ig_data, yt_data),
            "top_content": self._get_top_content(ig_data, yt_data),
            "ai_suggestions": self._generate_ai_suggestions(ig_data)
        }

    def _today_vs_previous(self, df: pd.DataFrame) -> dict:
        if df.empty or 'upload_date' not in df.columns:
            return {}

        x = df.copy()
        x['date_only'] = x['upload_date'].dt.date
        daily = x.groupby('date_only').agg({'likes': 'sum', 'comments': 'sum', 'shares': 'sum', 'engagement_rate': 'mean'})
        if len(daily) < 2:
            return {}

        latest = daily.iloc[-1]
        prev = daily.iloc[-2]

        def pct(curr, old):
            base = old if old != 0 else 1
            return round(((curr - old) / base) * 100, 2)

        return {
            'today': {
                'likes': int(latest['likes']),
                'comments': int(latest['comments']),
                'shares': int(latest['shares']),
                'engagement_rate': round(float(latest['engagement_rate']), 2),
            },
            'previous': {
                'likes': int(prev['likes']),
                'comments': int(prev['comments']),
                'shares': int(prev['shares']),
                'engagement_rate': round(float(prev['engagement_rate']), 2),
            },
            'delta_percent': {
                'likes': pct(latest['likes'], prev['likes']),
                'comments': pct(latest['comments'], prev['comments']),
                'shares': pct(latest['shares'], prev['shares']),
                'engagement_rate': pct(latest['engagement_rate'], prev['engagement_rate']),
            },
        }

    def _graph_ready_series(self, df: pd.DataFrame) -> dict:
        if df.empty or 'upload_date' not in df.columns:
            return {'daily': [], 'hourly': []}

        x = df.copy()
        x['date_only'] = x['upload_date'].dt.date
        daily = x.groupby('date_only').agg({'likes': 'sum', 'comments': 'sum', 'shares': 'sum', 'reach': 'sum', 'engagement_rate': 'mean'}).tail(30)
        daily_series = [
            {
                'date': str(idx),
                'likes': int(row['likes']),
                'comments': int(row['comments']),
                'shares': int(row['shares']),
                'reach': int(row['reach']),
                'engagement_rate': round(float(row['engagement_rate']), 2),
            }
            for idx, row in daily.iterrows()
        ]

        if 'upload_hour' in x.columns:
            hourly = x.groupby('upload_hour').agg({'engagement_rate': 'mean', 'likes': 'mean'}).reset_index()
            hourly_series = [
                {
                    'hour': int(row['upload_hour']),
                    'engagement_rate': round(float(row['engagement_rate']), 2),
                    'likes': round(float(row['likes']), 2),
                }
                for _, row in hourly.iterrows()
            ]
        else:
            hourly_series = []

        return {'daily': daily_series, 'hourly': hourly_series}
    
    def _get_overview(self, ig: pd.DataFrame, yt: pd.DataFrame) -> dict:
        overview = {
            "total_posts": 0,
            "total_reach": 0,
            "total_engagement": 0,
            "avg_engagement_rate": 0,
            "total_followers_gained": 0
        }
        
        if not ig.empty:
            overview["total_posts"] += len(ig)
            overview["total_reach"] += int(ig['reach'].sum())
            overview["total_engagement"] += int(ig[['likes', 'comments', 'shares', 'saves']].sum().sum())
            overview["avg_engagement_rate"] = round(ig['engagement_rate'].mean(), 2)
            overview["total_followers_gained"] = int(ig['followers_gained'].sum())
        
        if not yt.empty:
            overview["total_posts"] += len(yt)
            overview["total_reach"] += int(yt['Views'].sum())
            overview["total_engagement"] += int(yt[['Likes', 'Comments']].sum().sum())
        
        return overview
    
    def _get_engagement_metrics(self, df: pd.DataFrame) -> dict:
        if df.empty:
            return {}
        
        metrics = {
            "likes": {
                "total": int(df['likes'].sum()),
                "average": int(df['likes'].mean()),
                "max": int(df['likes'].max()),
                "trend": self._calc_trend(df, 'likes')
            },
            "comments": {
                "total": int(df['comments'].sum()),
                "average": int(df['comments'].mean()),
                "max": int(df['comments'].max()),
                "trend": self._calc_trend(df, 'comments')
            },
            "shares": {
                "total": int(df['shares'].sum()),
                "average": int(df['shares'].mean()),
                "max": int(df['shares'].max()),
                "trend": self._calc_trend(df, 'shares')
            },
            "saves": {
                "total": int(df['saves'].sum()),
                "average": int(df['saves'].mean()),
                "max": int(df['saves'].max()),
                "trend": self._calc_trend(df, 'saves')
            },
            "engagement_rate": {
                "average": round(df['engagement_rate'].mean(), 2),
                "median": round(df['engagement_rate'].median(), 2),
                "max": round(df['engagement_rate'].max(), 2),
                "distribution": self._get_engagement_distribution(df)
            }
        }
        return metrics
    
    def _get_growth_trends(self, df: pd.DataFrame) -> dict:
        if df.empty or 'upload_date' not in df.columns:
            return {}
        
        df_sorted = df.sort_values('upload_date')
        
        # Monthly trends
        df_sorted['month'] = df_sorted['upload_date'].dt.to_period('M')
        monthly = df_sorted.groupby('month').agg({
            'likes': 'sum',
            'comments': 'sum',
            'shares': 'sum',
            'engagement_rate': 'mean',
            'followers_gained': 'sum',
            'post_id': 'count'
        }).rename(columns={'post_id': 'post_count'})
        
        monthly_data = []
        for period, row in monthly.iterrows():
            monthly_data.append({
                "month": str(period),
                "total_likes": int(row['likes']),
                "total_comments": int(row['comments']),
                "total_shares": int(row['shares']),
                "avg_engagement_rate": round(row['engagement_rate'], 2),
                "followers_gained": int(row['followers_gained']),
                "post_count": int(row['post_count'])
            })
        
        # Weekly trends
        df_sorted['week'] = df_sorted['upload_date'].dt.isocalendar().week
        weekly = df_sorted.groupby('week').agg({
            'engagement_rate': 'mean',
            'likes': 'sum'
        })
        
        weekly_data = [{"week": int(w), "avg_engagement": round(row['engagement_rate'], 2), 
                       "total_likes": int(row['likes'])} for w, row in weekly.iterrows()]
        
        # Day of week analysis
        if 'upload_day' in df.columns:
            dow = df.groupby('upload_day')['engagement_rate'].mean().sort_values(ascending=False)
            day_analysis = [{"day": d, "avg_engagement": round(e, 2)} for d, e in dow.items()]
        else:
            day_analysis = []
        
        return {
            "monthly": monthly_data[-12:],  # Last 12 months
            "weekly": weekly_data[-8:],  # Last 8 weeks
            "by_day_of_week": day_analysis
        }
    
    def _get_peak_hours(self, ig: pd.DataFrame, yt: pd.DataFrame) -> dict:
        result = {}
        
        if not ig.empty and 'upload_hour' in ig.columns:
            ig_hours = ig.groupby('upload_hour').agg({
                'engagement_rate': 'mean',
                'likes': 'mean',
                'reach': 'mean'
            }).sort_values('engagement_rate', ascending=False)
            
            result["instagram"] = [
                {"hour": int(h), "avg_engagement": round(row['engagement_rate'], 2),
                 "avg_likes": int(row['likes']), "avg_reach": int(row['reach'])}
                for h, row in ig_hours.head(8).iterrows()
            ]
        
        if not yt.empty and 'Posting_Hour' in yt.columns:
            yt_hours = yt.groupby('Posting_Hour').agg({
                'Views': 'mean',
                'Likes': 'mean'
            }).sort_values('Views', ascending=False)
            
            result["youtube"] = [
                {"hour": int(h), "avg_views": int(row['Views']), "avg_likes": int(row['Likes'])}
                for h, row in yt_hours.head(8).iterrows()
            ]
        
        return result
    
    def _get_platform_comparison(self, ig: pd.DataFrame, yt: pd.DataFrame) -> dict:
        comparison = {}
        
        if not ig.empty:
            comparison["instagram"] = {
                "total_posts": len(ig),
                "avg_engagement_rate": round(ig['engagement_rate'].mean(), 2),
                "total_likes": int(ig['likes'].sum()),
                "total_reach": int(ig['reach'].sum()),
                "best_content_type": ig.groupby('media_type')['engagement_rate'].mean().idxmax() if 'media_type' in ig.columns else "N/A",
                "best_category": ig.groupby('content_category')['engagement_rate'].mean().idxmax() if 'content_category' in ig.columns else "N/A"
            }
        
        if not yt.empty:
            comparison["youtube"] = {
                "total_videos": len(yt),
                "total_views": int(yt['Views'].sum()),
                "total_likes": int(yt['Likes'].sum()),
                "avg_views": int(yt['Views'].mean()),
                "avg_likes": int(yt['Likes'].mean()),
                "top_channel": yt.nlargest(1, 'Views')['Channel'].values[0] if 'Channel' in yt.columns else "N/A"
            }
        
        return comparison
    
    def _get_top_content(self, ig: pd.DataFrame, yt: pd.DataFrame) -> dict:
        top = {}
        
        if not ig.empty:
            top_ig = ig.nlargest(10, 'engagement_rate')
            top["instagram"] = [{
                "post_id": str(row.get('post_id', '')),
                "media_type": str(row.get('media_type', '')),
                "likes": int(row.get('likes', 0)),
                "comments": int(row.get('comments', 0)),
                "shares": int(row.get('shares', 0)),
                "engagement_rate": round(row.get('engagement_rate', 0), 2),
                "category": str(row.get('content_category', ''))
            } for _, row in top_ig.iterrows()]
        
        if not yt.empty:
            top_yt = yt.nlargest(10, 'Views')
            top["youtube"] = [{
                "title": str(row.get('Title', ''))[:80],
                "channel": str(row.get('Channel', '')),
                "views": int(row.get('Views', 0)),
                "likes": int(row.get('Likes', 0)),
                "comments": int(row.get('Comments', 0))
            } for _, row in top_yt.iterrows()]
        
        return top
    
    def _generate_ai_suggestions(self, df: pd.DataFrame) -> list:
        suggestions = []
        if df.empty:
            return ["No data available for analysis"]
        
        # Analyze content types
        if 'media_type' in df.columns:
            best_type = df.groupby('media_type')['engagement_rate'].mean().idxmax()
            suggestions.append(f"📈 Focus more on {best_type}s — they have the highest average engagement")
        
        # Analyze posting times
        if 'upload_hour' in df.columns:
            best_hour = df.groupby('upload_hour')['engagement_rate'].mean().idxmax()
            suggestions.append(f"⏰ Best posting time: {int(best_hour)}:00 — schedule posts around this time")
        
        # Analyze categories
        if 'content_category' in df.columns:
            top_cats = df.groupby('content_category')['engagement_rate'].mean().nlargest(3)
            cats = ", ".join(top_cats.index.tolist())
            suggestions.append(f"🎯 Top performing niches: {cats} — create more content in these areas")
        
        # Analyze hashtags
        if 'hashtags_count' in df.columns:
            optimal_hashtags = df.groupby(pd.cut(df['hashtags_count'], bins=[0, 5, 10, 15, 20, 30]))['engagement_rate'].mean()
            best_range = optimal_hashtags.idxmax()
            suggestions.append(f"#️⃣ Optimal hashtag count: {best_range} hashtags per post")
        
        # Caption length analysis
        if 'caption_length' in df.columns:
            optimal_caption = df.groupby(pd.cut(df['caption_length'], bins=[0, 200, 500, 1000, 1500, 2500]))['engagement_rate'].mean()
            best_len = optimal_caption.idxmax()
            suggestions.append(f"📝 Best caption length: {best_len} characters")
        
        # Traffic source
        if 'traffic_source' in df.columns:
            best_source = df.groupby('traffic_source')['reach'].sum().idxmax()
            suggestions.append(f"🔗 Most effective traffic source: {best_source}")
        
        suggestions.append("🔄 Maintain consistent posting schedule for algorithm favor")
        suggestions.append("💬 Reply to comments within 1 hour to boost engagement")
        
        return suggestions
    
    def _calc_trend(self, df, column):
        if df.empty or 'upload_date' not in df.columns:
            return "stable"
        df_sorted = df.sort_values('upload_date')
        half = len(df_sorted) // 2
        first_half = df_sorted[column].iloc[:half].mean()
        second_half = df_sorted[column].iloc[half:].mean()
        if second_half > first_half * 1.1:
            return "↑ increasing"
        elif second_half < first_half * 0.9:
            return "↓ decreasing"
        return "→ stable"
    
    def _get_engagement_distribution(self, df):
        if 'engagement_rate' not in df.columns:
            return {}
        bins = [0, 2, 5, 10, 20, 50, float('inf')]
        labels = ['0-2%', '2-5%', '5-10%', '10-20%', '20-50%', '50%+']
        dist = pd.cut(df['engagement_rate'], bins=bins, labels=labels).value_counts()
        return {str(k): int(v) for k, v in dist.items()}
    
    def get_content_analytics(self, content_type: str = None, category: str = None) -> dict:
        """Get filtered analytics by content type or category."""
        df = pipeline.get_instagram_data()
        if df.empty:
            return {}
        
        if content_type:
            df = df[df['media_type'] == content_type]
        if category:
            df = df[df['content_category'] == category]
        
        return {
            "filtered_count": len(df),
            "engagement": self._get_engagement_metrics(df),
            "top_content": self._get_top_content(df, pd.DataFrame()),
            "suggestions": self._generate_ai_suggestions(df)
        }


# Global instance  
analytics_engine = AnalyticsEngine()
