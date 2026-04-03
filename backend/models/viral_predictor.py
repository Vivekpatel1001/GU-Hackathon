"""
Viral Prediction Model - ML model for predicting content virality score (0-100).
Uses RandomForest and XGBoost with feature engineering.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import joblib
import logging
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from backend.config import VIRAL_MODEL_PATH, SCALER_PATH, MODEL_DIR
from backend.data.pipeline import pipeline

logger = logging.getLogger(__name__)


class ViralPredictor:
    """ML model for predicting content virality score."""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.is_trained = False
        self._try_load_model()
    
    def _try_load_model(self):
        """Try to load a pre-trained model."""
        try:
            if VIRAL_MODEL_PATH.exists() and SCALER_PATH.exists():
                self.model = joblib.load(VIRAL_MODEL_PATH)
                self.scaler = joblib.load(SCALER_PATH)
                le_path = MODEL_DIR / "label_encoders.pkl"
                fn_path = MODEL_DIR / "feature_names.pkl"
                if le_path.exists():
                    self.label_encoders = joblib.load(le_path)
                if fn_path.exists():
                    self.feature_names = joblib.load(fn_path)
                self.is_trained = True
                logger.info("✅ Pre-trained viral model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load pre-trained model: {e}")
    
    def train(self) -> dict:
        """Train the viral prediction model on Instagram data."""
        logger.info("🏋️ Training Viral Prediction Model...")
        
        df = pipeline.get_instagram_data()
        if df.empty:
            raise ValueError("No Instagram data available for training")
        
        # Feature Engineering
        df = self._engineer_features(df)
        
        # Create virality score (0-100)
        df['viral_score'] = self._calculate_viral_score(df)
        
        # Select features
        feature_cols = [
            'likes', 'comments', 'shares', 'saves', 'reach', 'impressions',
            'caption_length', 'hashtags_count', 'followers_gained',
            'upload_hour', 'upload_month', 'media_type_encoded',
            'content_category_encoded', 'traffic_source_encoded',
            'total_engagement', 'engagement_per_reach', 'save_rate',
            'comment_to_like_ratio', 'is_weekend'
        ]
        
        available_features = [c for c in feature_cols if c in df.columns]
        self.feature_names = available_features
        
        X = df[available_features].fillna(0)
        y = df['viral_score'].clip(0, 100)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train Gradient Boosting (better than simple RF)
        self.model = GradientBoostingRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42
        )
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        y_pred = np.clip(y_pred, 0, 100)
        
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Save model
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, VIRAL_MODEL_PATH)
        joblib.dump(self.scaler, SCALER_PATH)
        joblib.dump(self.label_encoders, MODEL_DIR / "label_encoders.pkl")
        joblib.dump(self.feature_names, MODEL_DIR / "feature_names.pkl")
        
        self.is_trained = True
        
        metrics = {
            "mae": round(mae, 2),
            "r2_score": round(r2, 4),
            "rmse": round(rmse, 2),
            "samples_trained": len(X_train),
            "samples_tested": len(X_test),
            "features_used": len(available_features),
            "model_type": "GradientBoostingRegressor"
        }
        
        logger.info(f"✅ Model trained! MAE: {mae:.2f}, R2: {r2:.4f}")
        return metrics
    
    def predict(self, features: dict) -> dict:
        """Predict virality score for given features."""
        if not self.is_trained:
            self.train()
        
        # Prepare feature vector
        feature_vector = self._prepare_features(features)
        
        # Scale and predict
        feature_scaled = self.scaler.transform([feature_vector])
        score = self.model.predict(feature_scaled)[0]
        score = np.clip(score, 0, 100)
        
        # Generate insights
        insights = self._generate_insights(features, score)
        
        return {
            "viral_score": round(float(score), 1),
            "viral_level": self._get_viral_level(score),
            "confidence": self._get_confidence(score),
            "insights": insights,
            "improvement_tips": self._get_improvement_tips(features, score)
        }
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create engineered features."""
        # Encode categorical variables
        categorical_cols = ['media_type', 'content_category', 'traffic_source']
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
        
        # Engagement features
        df['total_engagement'] = df.get('likes', 0) + df.get('comments', 0) + df.get('shares', 0) + df.get('saves', 0)
        df['engagement_per_reach'] = df['total_engagement'] / df.get('reach', 1).replace(0, 1) * 100
        df['save_rate'] = df.get('saves', 0) / df.get('reach', 1).replace(0, 1) * 100
        df['comment_to_like_ratio'] = df.get('comments', 0) / df.get('likes', 1).replace(0, 1)
        
        # Time features
        if 'upload_date' in df.columns:
            df['is_weekend'] = df['upload_date'].dt.dayofweek.isin([5, 6]).astype(int)
        else:
            df['is_weekend'] = 0
        
        return df
    
    def _calculate_viral_score(self, df: pd.DataFrame) -> pd.Series:
        """Calculate viral score (0-100) based on engagement metrics."""
        scores = pd.Series(0.0, index=df.index)
        
        # Weighted scoring
        if 'engagement_rate' in df.columns:
            scores += np.clip(df['engagement_rate'] * 2, 0, 30)
        if 'likes' in df.columns:
            scores += np.clip(df['likes'].rank(pct=True) * 25, 0, 25)
        if 'shares' in df.columns:
            scores += np.clip(df['shares'].rank(pct=True) * 20, 0, 20)
        if 'comments' in df.columns:
            scores += np.clip(df['comments'].rank(pct=True) * 15, 0, 15)
        if 'followers_gained' in df.columns:
            scores += np.clip(df['followers_gained'].rank(pct=True) * 10, 0, 10)
        
        return np.clip(scores, 0, 100)
    
    def _prepare_features(self, features: dict) -> list:
        """Prepare feature vector from input dict."""
        vector = []
        for fname in self.feature_names:
            if fname in features:
                vector.append(float(features[fname]))
            elif fname.endswith('_encoded'):
                base_name = fname.replace('_encoded', '')
                if base_name in features and base_name in self.label_encoders:
                    try:
                        val = self.label_encoders[base_name].transform([features[base_name]])[0]
                    except ValueError:
                        val = 0
                    vector.append(float(val))
                else:
                    vector.append(0.0)
            else:
                vector.append(0.0)
        return vector
    
    @staticmethod
    def _get_viral_level(score: float) -> str:
        if score >= 80: return "🔥 VIRAL"
        elif score >= 60: return "📈 HIGH POTENTIAL"
        elif score >= 40: return "✨ MODERATE"
        elif score >= 20: return "📊 LOW"
        else: return "❄️ VERY LOW"
    
    @staticmethod
    def _get_confidence(score: float) -> str:
        if score >= 70 or score <= 20: return "HIGH"
        elif score >= 50 or score <= 35: return "MEDIUM"
        else: return "LOW"
    
    @staticmethod
    def _generate_insights(features: dict, score: float) -> list:
        insights = []
        if features.get('hashtags_count', 0) < 5:
            insights.append("Add more relevant hashtags (aim for 10-15)")
        if features.get('hashtags_count', 0) > 25:
            insights.append("Reduce hashtags - too many can reduce reach")
        if features.get('caption_length', 0) < 50:
            insights.append("Write a longer, more engaging caption")
        if features.get('caption_length', 0) > 2000:
            insights.append("Consider shortening your caption for better engagement")
        posting_hour = features.get('upload_hour', features.get('posting_hour', 12))
        if posting_hour < 7 or posting_hour > 22:
            insights.append("Post during peak hours (9-11 AM or 7-9 PM)")
        if score < 40:
            insights.append("Consider using trending audio/topics to boost visibility")
        return insights
    
    @staticmethod
    def _get_improvement_tips(features: dict, score: float) -> list:
        tips = []
        if score < 60:
            tips.append("Use eye-catching thumbnails/first frames")
            tips.append("Add a strong hook in the first 3 seconds")
            tips.append("Engage with comments within the first hour")
        if score < 40:
            tips.append("Collaborate with creators in your niche")
            tips.append("Use trending sounds and formats")
            tips.append("Post consistently at your peak engagement times")
        if score >= 60:
            tips.append("Great content! Consider cross-posting to other platforms")
            tips.append("Create a follow-up to maintain momentum")
        return tips


# Global predictor instance
viral_predictor = ViralPredictor()
