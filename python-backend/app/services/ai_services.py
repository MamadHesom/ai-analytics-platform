"""AI and ML business services used by the API routers."""

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest

from app.services.data_processing import numeric_features


class ModelInferenceError(RuntimeError):
    """Raised when a configured model cannot produce a prediction."""


class AnomalyDetectionService:
    """Fit an Isolation Forest for request-scoped anomaly scoring."""

    def detect(
        self,
        records: list[dict[str, Any]],
        contamination: float,
        feature_columns: list[str] | None = None,
        random_state: int = 42,
    ) -> dict[str, Any]:
        features, selected = numeric_features(records, feature_columns)
        estimator = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=200,
            n_jobs=-1,
        )
        labels = estimator.fit_predict(features)
        scores = estimator.decision_function(features)
        anomalies = [
            {
                "index": int(index),
                "is_anomaly": bool(label == -1),
                "anomaly_score": round(float(score), 6),
                "features": {column: round(float(value), 6) for column, value in row.items()},
            }
            for index, (label, score, row) in enumerate(
                zip(labels, scores, features.to_dict(orient="records"), strict=True)
            )
        ]
        return {
            "model": "isolation_forest",
            "contamination": contamination,
            "feature_columns": selected,
            "anomalies": anomalies,
            "anomaly_count": sum(item["is_anomaly"] for item in anomalies),
        }


class PredictionService:
    """Load and execute a persisted scikit-learn pipeline."""

    def __init__(self, artifact_path: str, target_name: str = "target") -> None:
        self.artifact_path = Path(artifact_path)
        self.target_name = target_name
        self._model: Any | None = None

    @property
    def model_loaded(self) -> bool:
        return self._model is not None

    def load(self) -> None:
        if not self.artifact_path.exists():
            raise ModelInferenceError(f"Model artifact not found: {self.artifact_path}")
        try:
            self._model = joblib.load(self.artifact_path)
        except Exception as exc:  # pragma: no cover - exact backend exception varies by artifact
            raise ModelInferenceError("Unable to load model artifact") from exc

    def predict(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        if self._model is None:
            self.load()
        try:
            frame = pd.DataFrame.from_records(records)
            predictions = self._model.predict(frame)
        except Exception as exc:
            raise ModelInferenceError("Model could not score the supplied records") from exc
        return {
            "model_name": type(self._model).__name__,
            "predictions": [float(value) for value in predictions],
            "model_loaded": True,
        }


class SentimentService:
    """Explainable, dependency-light sentiment scoring for short text."""

    POSITIVE = {
        "amazing",
        "benefit",
        "brilliant",
        "excellent",
        "fast",
        "good",
        "great",
        "happy",
        "helpful",
        "improve",
        "love",
        "positive",
        "reliable",
        "smooth",
        "success",
        "thank",
        "useful",
        "wonderful",
    }
    NEGATIVE = {
        "awful",
        "bad",
        "broken",
        "delay",
        "difficult",
        "error",
        "fail",
        "frustrating",
        "hate",
        "late",
        "negative",
        "poor",
        "problem",
        "slow",
        "terrible",
        "unhelpful",
        "worst",
    }

    def analyze(self, text: str) -> dict[str, Any]:
        tokens = {token.strip(".,!?;:()[]{}\"'").lower() for token in text.split()}
        positive = sorted(tokens & self.POSITIVE)
        negative = sorted(tokens & self.NEGATIVE)
        score = max(-1.0, min(1.0, (len(positive) - len(negative)) / max(len(tokens), 1) * 4))
        label = "positive" if score > 0.1 else "negative" if score < -0.1 else "neutral"
        return {
            "text": text,
            "label": label,
            "score": round(score, 6),
            "positive_terms": positive,
            "negative_terms": negative,
        }

    def analyze_batch(self, texts: list[str]) -> dict[str, Any]:
        results = [self.analyze(text) for text in texts]
        average = sum(item["score"] for item in results) / len(results)
        aggregate = "positive" if average > 0.1 else "negative" if average < -0.1 else "neutral"
        return {"results": results, "aggregate_label": aggregate, "average_score": round(average, 6)}
