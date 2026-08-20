"""Pydantic request and response contracts for the analytics API."""

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class RecordSetRequest(BaseModel):
    """A bounded collection of JSON-like records."""

    records: list[dict[str, Any]] = Field(min_length=1)

    @field_validator("records")
    @classmethod
    def reject_empty_records(cls, value: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if any(not record for record in value):
            raise ValueError("records must not contain empty objects")
        return value


class SummaryResponse(BaseModel):
    rows: int
    columns: list[str]
    numeric_summary: dict[str, dict[str, float | int | None]]
    missing_values: dict[str, int]
    categorical_cardinality: dict[str, int]


class AnomalyRequest(RecordSetRequest):
    contamination: float = Field(default=0.05, gt=0, lt=0.5)
    feature_columns: list[str] | None = None


class AnomalyRecord(BaseModel):
    index: int
    is_anomaly: bool
    anomaly_score: float
    features: dict[str, float]


class AnomalyResponse(BaseModel):
    model: Literal["isolation_forest"]
    contamination: float
    feature_columns: list[str]
    anomalies: list[AnomalyRecord]
    anomaly_count: int


class PredictionRequest(BaseModel):
    records: list[dict[str, Any]] = Field(min_length=1)


class PredictionResponse(BaseModel):
    model_name: str
    predictions: list[float]
    model_loaded: bool


class SentimentRequest(BaseModel):
    texts: list[str] = Field(min_length=1)

    @field_validator("texts")
    @classmethod
    def validate_texts(cls, value: list[str]) -> list[str]:
        cleaned = [text.strip() for text in value]
        if any(not text for text in cleaned):
            raise ValueError("texts must contain non-empty strings")
        return cleaned


class SentimentItem(BaseModel):
    text: str
    label: Literal["positive", "neutral", "negative"]
    score: float = Field(ge=-1, le=1)
    positive_terms: list[str]
    negative_terms: list[str]


class SentimentResponse(BaseModel):
    results: list[SentimentItem]
    aggregate_label: Literal["positive", "neutral", "negative"]
    average_score: float = Field(ge=-1, le=1)


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str
    environment: str


class ErrorResponse(BaseModel):
    detail: str
    request_id: str
