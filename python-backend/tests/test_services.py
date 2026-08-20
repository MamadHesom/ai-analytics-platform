from pathlib import Path

import pytest
from app.services.ai_services import AnomalyDetectionService, ModelInferenceError, PredictionService, SentimentService
from app.services.data_processing import DataProcessingError, numeric_features, summarize_records


def test_summary_handles_mixed_records() -> None:
    result = summarize_records(
        [
            {"revenue": 100, "region": "west"},
            {"revenue": 200, "region": "east"},
            {"revenue": None, "region": "west"},
        ]
    )
    assert result["rows"] == 3
    assert result["missing_values"]["revenue"] == 1
    assert result["categorical_cardinality"]["region"] == 2
    assert result["numeric_summary"]["revenue"]["mean"] == pytest.approx(150.0)


def test_numeric_features_impute_missing_values() -> None:
    frame, columns = numeric_features([{"x": 1}, {"x": None}, {"x": 3}])
    assert columns == ["x"]
    assert frame["x"].tolist() == [1.0, 2.0, 3.0]


def test_numeric_features_requires_numeric_column() -> None:
    with pytest.raises(DataProcessingError):
        numeric_features([{"region": "west"}])


def test_anomaly_service_returns_one_result_per_record() -> None:
    result = AnomalyDetectionService().detect(
        [{"latency": 10}, {"latency": 11}, {"latency": 12}, {"latency": 1000}],
        contamination=0.25,
    )
    assert len(result["anomalies"]) == 4
    assert result["anomaly_count"] >= 1


def test_sentiment_service_is_explainable() -> None:
    result = SentimentService().analyze("Excellent and helpful support")
    assert result["label"] == "positive"
    assert "excellent" in result["positive_terms"]


def test_prediction_service_reports_missing_artifact() -> None:
    service = PredictionService(str(Path("/does/not/exist.joblib")))
    with pytest.raises(ModelInferenceError, match="not found"):
        service.predict([{"x": 1}])
