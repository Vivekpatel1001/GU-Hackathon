"""Data pipeline with CSV + SQLite persistence and resilient source ingestion."""

import logging
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.config import (  # noqa: E402
    DATA_DIR,
    DB_PATH,
    INSTAGRAM_CSV,
    PIPELINE_TWITTER_ROWS,
    TWITTER_CSV,
    YOUTUBE_CSV,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DataPipeline:
    """Robust pipeline for loading, cleaning, and storing social media data."""

    def __init__(self):
        self.instagram_data = None
        self.youtube_data = None
        self.twitter_data = None

    def run(self):
        """Run the complete pipeline in one command."""
        logger.info("Starting Data Pipeline")

        self.instagram_data = self._load_instagram()
        self.youtube_data = self._load_youtube()
        self.twitter_data = self._load_twitter()

        self.instagram_data = self._clean_instagram(self.instagram_data)
        self.youtube_data = self._clean_youtube(self.youtube_data)
        self.twitter_data = self._clean_twitter(self.twitter_data)

        self._save_cleaned_data()
        self._save_to_sqlite()

        logger.info("Pipeline completed successfully")
        return {
            "instagram": len(self.instagram_data),
            "youtube": len(self.youtube_data),
            "twitter": len(self.twitter_data),
            "db_path": str(DB_PATH),
        }

    def _load_instagram(self) -> pd.DataFrame:
        """Load Instagram analytics data with fallback handling."""
        try:
            df = pd.read_csv(INSTAGRAM_CSV)
            logger.info("Loaded Instagram data: %s rows, %s columns", len(df), len(df.columns))
            return df
        except FileNotFoundError:
            logger.error("Instagram CSV not found at %s", INSTAGRAM_CSV)
            return pd.DataFrame()
        except Exception as e:
            logger.error("Error loading Instagram data: %s", e)
            return pd.DataFrame()

    def _load_youtube(self) -> pd.DataFrame:
        """Load YouTube trending data with fallback handling."""
        try:
            df = pd.read_csv(YOUTUBE_CSV)
            logger.info("Loaded YouTube data: %s rows, %s columns", len(df), len(df.columns))
            return df
        except FileNotFoundError:
            logger.error("YouTube CSV not found at %s", YOUTUBE_CSV)
            return pd.DataFrame()
        except Exception as e:
            logger.error("Error loading YouTube data: %s", e)
            return pd.DataFrame()

    def _load_twitter(self) -> pd.DataFrame:
        """Load Twitter sentiment data with fallback handling."""
        try:
            df = pd.read_csv(
                TWITTER_CSV,
                encoding="latin-1",
                header=None,
                names=["sentiment", "id", "date", "query", "user", "text"],
                nrows=PIPELINE_TWITTER_ROWS,
            )
            logger.info("Loaded Twitter data: %s rows", len(df))
            return df
        except FileNotFoundError:
            logger.error("Twitter CSV not found at %s", TWITTER_CSV)
            return pd.DataFrame()
        except Exception as e:
            logger.error("Error loading Twitter data: %s", e)
            return pd.DataFrame()

    def _clean_instagram(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean Instagram data."""
        if df.empty:
            return df
        logger.info("Cleaning Instagram data")

        numeric_cols = [
            "likes",
            "comments",
            "shares",
            "saves",
            "reach",
            "impressions",
            "caption_length",
            "hashtags_count",
            "followers_gained",
            "engagement_rate",
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        if "upload_date" in df.columns:
            df["upload_date"] = pd.to_datetime(df["upload_date"], errors="coerce")
            df["upload_hour"] = df["upload_date"].dt.hour.fillna(0).astype(int)
            df["upload_day"] = df["upload_date"].dt.day_name().fillna("Unknown")
            df["upload_month"] = df["upload_date"].dt.month.fillna(1).astype(int)

        if "post_id" in df.columns:
            df = df.drop_duplicates(subset=["post_id"], keep="first")
        else:
            df = df.drop_duplicates(keep="first")

        logger.info("Instagram data cleaned: %s rows remaining", len(df))
        return df

    def _clean_youtube(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean YouTube data."""
        if df.empty:
            return df
        logger.info("Cleaning YouTube data")

        if "Title" in df.columns:
            df["Title_Clean"] = df["Title"].apply(self._clean_text)

        numeric_cols = ["Views", "Likes", "Comments", "Hashtags_Count", "Caption_Length", "Posting_Hour"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        if "Views" in df.columns and "Likes" in df.columns:
            df["Like_Rate"] = (df["Likes"] / df["Views"].replace(0, 1)) * 100
            df["Comment_Rate"] = (df.get("Comments", 0) / df["Views"].replace(0, 1)) * 100
            df["Engagement_Score"] = df["Like_Rate"] + df["Comment_Rate"] * 2

        logger.info("YouTube data cleaned: %s rows remaining", len(df))
        return df

    def _clean_twitter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean Twitter data."""
        if df.empty:
            return df
        logger.info("Cleaning Twitter data")

        if "text" in df.columns:
            df["text_clean"] = df["text"].apply(self._clean_text)
            df["text_length"] = df["text_clean"].str.len().fillna(0).astype(int)
            df["word_count"] = df["text_clean"].str.split().str.len().fillna(0).astype(int)

        if "sentiment" in df.columns:
            df["sentiment_label"] = df["sentiment"].map({0: "negative", 4: "positive"}).fillna("neutral")

        df = df[df["text_clean"].str.len() > 5] if "text_clean" in df.columns else df

        logger.info("Twitter data cleaned: %s rows remaining", len(df))
        return df

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean text by removing emojis, special chars, normalizing."""
        if not isinstance(text, str):
            return ""
        text = re.sub(r"http\S+|www\.\S+", "", text)
        text = re.sub(r"@\w+", "", text)
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE,
        )
        text = emoji_pattern.sub("", text)
        text = re.sub(r"[^\w\s.,!?#\'-]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _save_cleaned_data(self):
        """Save all cleaned data."""
        try:
            cleaned_dir = DATA_DIR / "cleaned"
            cleaned_dir.mkdir(exist_ok=True)

            if not self.instagram_data.empty:
                self.instagram_data.to_csv(cleaned_dir / "instagram_cleaned.csv", index=False)
            if not self.youtube_data.empty:
                self.youtube_data.to_csv(cleaned_dir / "youtube_cleaned.csv", index=False)
            if not self.twitter_data.empty:
                self.twitter_data.to_csv(cleaned_dir / "twitter_cleaned.csv", index=False)

            logger.info("Cleaned data saved to %s", cleaned_dir)
        except Exception as e:
            logger.error("Error saving cleaned data: %s", e)

    def _save_to_sqlite(self):
        """Persist cleaned datasets into SQLite for API query scenarios."""
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            if self.instagram_data is not None and not self.instagram_data.empty:
                self.instagram_data.to_sql("instagram_cleaned", conn, if_exists="replace", index=False)
            if self.youtube_data is not None and not self.youtube_data.empty:
                self.youtube_data.to_sql("youtube_cleaned", conn, if_exists="replace", index=False)
            if self.twitter_data is not None and not self.twitter_data.empty:
                self.twitter_data.to_sql("twitter_cleaned", conn, if_exists="replace", index=False)
        logger.info("SQLite persistence complete at %s", DB_PATH)

    def query_sqlite(self, sql: str, params: tuple[Any, ...] | None = None) -> pd.DataFrame:
        """Run lightweight read queries against local SQLite storage."""
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query(sql, conn, params=params)

    def get_instagram_data(self) -> pd.DataFrame:
        if self.instagram_data is None:
            self.instagram_data = self._clean_instagram(self._load_instagram())
        return self.instagram_data

    def get_youtube_data(self) -> pd.DataFrame:
        if self.youtube_data is None:
            self.youtube_data = self._clean_youtube(self._load_youtube())
        return self.youtube_data

    def get_twitter_data(self) -> pd.DataFrame:
        if self.twitter_data is None:
            self.twitter_data = self._clean_twitter(self._load_twitter())
        return self.twitter_data


# Global pipeline instance
pipeline = DataPipeline()

if __name__ == "__main__":
    result = pipeline.run()
    print(f"\nPipeline Results: {result}")
