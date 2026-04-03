"""Video intelligence engine for frame-level quality and attention-drop analysis."""

from __future__ import annotations

import statistics
from pathlib import Path
from typing import Any

import cv2
import numpy as np


class VideoEngine:
    """Performs frame-level analysis and generates editing recommendations."""

    def analyze_image(self, image_path: str) -> dict[str, Any]:
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        image = cv2.imread(str(path))
        if image is None:
            raise ValueError("Unable to read image")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        height, width = gray.shape
        brightness = float(np.mean(gray))
        contrast = float(np.std(gray))
        sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        saturation = float(np.mean(hsv[:, :, 1]))

        center_crop = gray[height // 4 : (height * 3) // 4, width // 4 : (width * 3) // 4]
        edge_crop = gray[: height // 6, :] if height >= 6 else gray
        center_focus = float(np.std(center_crop)) if center_crop.size else 0.0
        top_clutter = float(np.std(edge_crop)) if edge_crop.size else 0.0

        quality_score = (
            0.32 * min(sharpness / 260.0, 1.0)
            + 0.26 * min(contrast / 55.0, 1.0)
            + 0.22 * (1.0 - min(abs(brightness - 135.0) / 135.0, 1.0))
            + 0.2 * min(saturation / 110.0, 1.0)
        ) * 100
        quality_score = round(float(max(0.0, min(100.0, quality_score))), 2)

        recommendations: list[str] = []
        if sharpness < 120:
            recommendations.append("Image looks soft. Use a sharper shot or improve camera stabilization.")
        if contrast < 35:
            recommendations.append("Boost contrast slightly so the subject stands out from the background.")
        if brightness < 85:
            recommendations.append("Image is underexposed. Increase lighting or raise exposure in editing.")
        if brightness > 195:
            recommendations.append("Highlights are too bright. Reduce exposure to recover details.")
        if saturation < 45:
            recommendations.append("Colors are muted. Increase saturation/vibrance for stronger visual impact.")
        if center_focus < 18:
            recommendations.append("Main subject is not prominent. Reframe so the subject is clearer in the center.")
        if top_clutter > 58:
            recommendations.append("Top frame looks busy. Simplify background to reduce distractions.")
        if not recommendations:
            recommendations.append("Image quality is strong. Only minor polish is needed before posting.")

        return {
            "summary": {
                "resolution": f"{width}x{height}",
                "brightness": round(brightness, 2),
                "contrast": round(contrast, 2),
                "sharpness": round(sharpness, 2),
                "saturation": round(saturation, 2),
            },
            "score": quality_score,
            "changes_needed": quality_score < 72,
            "verdict": "Changes recommended" if quality_score < 72 else "Looks good",
            "recommendations": recommendations,
        }

    def analyze_thumbnail(self, image_path: str) -> dict[str, Any]:
        base = self.analyze_image(image_path)
        score = float(base["score"])
        summary = base["summary"]

        brightness = float(summary["brightness"])
        contrast = float(summary["contrast"])
        saturation = float(summary["saturation"])

        clickability = (
            0.4 * min(contrast / 60.0, 1.0)
            + 0.35 * min(saturation / 120.0, 1.0)
            + 0.25 * (1.0 - min(abs(brightness - 145.0) / 145.0, 1.0))
        ) * 100
        clickability = round(float(max(0.0, min(100.0, clickability))), 2)

        seo_thumbnail_score = round(float((score * 0.6) + (clickability * 0.4)), 2)
        change_needed = seo_thumbnail_score < 75

        recommendations = list(base["recommendations"])
        if contrast < 42:
            recommendations.append("Use bolder text color contrast so the title is readable on mobile.")
        if saturation < 60:
            recommendations.append("Increase color separation to make the thumbnail pop in search results.")
        if brightness < 90 or brightness > 205:
            recommendations.append("Balance exposure for better readability in dark and bright themes.")

        return {
            "summary": summary,
            "thumbnail_score": seo_thumbnail_score,
            "quality_score": round(score, 2),
            "clickability_score": clickability,
            "changes_needed": change_needed,
            "verdict": "Needs improvement" if change_needed else "Strong thumbnail",
            "recommendations": recommendations,
        }

    def analyze_video(self, video_path: str, sample_step: int = 5) -> dict[str, Any]:
        path = Path(video_path)
        if not path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        cap = cv2.VideoCapture(str(path))
        if not cap.isOpened():
            raise ValueError("Unable to open video")

        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        duration = frame_count / max(fps, 1)

        frame_metrics: list[dict[str, float]] = []
        prev_gray = None
        idx = 0

        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if idx % sample_step != 0:
                idx += 1
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.Laplacian(gray, cv2.CV_64F).var()
            contrast = float(np.std(gray))
            brightness = float(np.mean(gray))

            motion = 0.0
            if prev_gray is not None:
                motion = float(np.mean(cv2.absdiff(gray, prev_gray)))

            scene_delta = motion + abs(brightness - (frame_metrics[-1]["brightness"] if frame_metrics else brightness))
            score = 0.45 * min(motion / 12.0, 1.0) + 0.35 * min(contrast / 70.0, 1.0) + 0.2 * min(blur / 500.0, 1.0)

            frame_metrics.append(
                {
                    "frame": float(idx),
                    "timestamp": round(idx / max(fps, 1), 2),
                    "motion": round(motion, 4),
                    "contrast": round(contrast, 4),
                    "brightness": round(brightness, 4),
                    "sharpness": round(float(blur), 4),
                    "scene_delta": round(float(scene_delta), 4),
                    "attention_score": round(float(score * 100), 2),
                }
            )
            prev_gray = gray
            idx += 1

        cap.release()

        if not frame_metrics:
            return {
                "summary": {"duration_sec": duration, "frames_analyzed": 0},
                "timeline": [],
                "drop_segments": [],
                "recommendations": ["Upload a valid video with readable frames."],
            }

        attention_scores = [m["attention_score"] for m in frame_metrics]
        threshold = max(25.0, statistics.mean(attention_scores) - statistics.pstdev(attention_scores))

        drops: list[dict[str, Any]] = []
        run_start = None
        for point in frame_metrics:
            low = point["attention_score"] < threshold
            if low and run_start is None:
                run_start = point
            if not low and run_start is not None:
                if point["timestamp"] - run_start["timestamp"] >= 2.0:
                    drops.append(
                        {
                            "start": run_start["timestamp"],
                            "end": point["timestamp"],
                            "reason": "Likely attention decline due to low motion/contrast pacing",
                        }
                    )
                run_start = None

        recommendations = self._build_recommendations(frame_metrics, drops)

        return {
            "summary": {
                "duration_sec": round(duration, 2),
                "fps": round(float(fps), 2),
                "frames_analyzed": len(frame_metrics),
                "avg_attention": round(float(statistics.mean(attention_scores)), 2),
            },
            "timeline": frame_metrics,
            "drop_segments": drops,
            "recommendations": recommendations,
        }

    def _build_recommendations(self, timeline: list[dict[str, float]], drops: list[dict[str, Any]]) -> list[str]:
        recs: list[str] = []
        avg_motion = statistics.mean([p["motion"] for p in timeline])
        avg_contrast = statistics.mean([p["contrast"] for p in timeline])
        avg_sharpness = statistics.mean([p["sharpness"] for p in timeline])

        if drops:
            recs.append("Trim or restructure low-attention segments highlighted in drop_segments.")
        if avg_motion < 6.5:
            recs.append("Increase pacing with quicker cuts, zoom transitions, or B-roll overlays.")
        if avg_contrast < 40:
            recs.append("Improve lighting and color grading to boost visual contrast.")
        if avg_sharpness < 120:
            recs.append("Use sharper shots or stabilize footage to improve perceived quality.")
        recs.append("Add a stronger hook within the first 3 seconds to reduce early drop-off.")

        return recs


video_engine = VideoEngine()
