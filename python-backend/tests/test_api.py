from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["X-Request-ID"]


def test_summary_endpoint() -> None:
    response = client.post(
        "/api/v1/analysis/summary",
        json={"records": [{"amount": 10, "team": "a"}, {"amount": 20, "team": "b"}]},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["rows"] == 2
    assert payload["numeric_summary"]["amount"]["mean"] == 15.0


def test_sentiment_endpoint() -> None:
    response = client.post(
        "/api/v1/analysis/sentiment",
        json={"texts": ["Great, fast service", "slow and frustrating"]},
    )
    assert response.status_code == 200
    assert response.json()["results"][0]["label"] == "positive"
    assert response.json()["results"][1]["label"] == "negative"


def test_anomaly_endpoint() -> None:
    response = client.post(
        "/api/v1/predictions/anomalies",
        json={"records": [{"x": 1}, {"x": 2}, {"x": 100}], "contamination": 0.34},
    )
    assert response.status_code == 200
    assert response.json()["feature_columns"] == ["x"]


def test_invalid_empty_text_is_rejected() -> None:
    response = client.post("/api/v1/analysis/sentiment", json={"texts": [""]})
    assert response.status_code == 422


def test_invalid_anomaly_contamination_is_rejected() -> None:
    response = client.post(
        "/api/v1/predictions/anomalies",
        json={"records": [{"x": 1}], "contamination": 0.9},
    )
    assert response.status_code == 422
