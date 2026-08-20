"""REST route definitions for health, analytics, and predictions."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import Settings, get_settings
from app.models.schemas import (
    AnomalyRequest,
    AnomalyResponse,
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
    RecordSetRequest,
    SentimentRequest,
    SentimentResponse,
    SummaryResponse,
)
from app.services.ai_services import AnomalyDetectionService, ModelInferenceError, PredictionService, SentimentService
from app.services.data_processing import DataProcessingError, summarize_records

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1")
settings_dependency = Annotated[Settings, Depends(get_settings)]
anomaly_service = AnomalyDetectionService()
sentiment_service = SentimentService()


@router.get("/health/live", response_model=HealthResponse, tags=["health"])
def liveness(settings: settings_dependency) -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name, version="1.0.0", environment=settings.environment)


@router.get("/health", response_model=HealthResponse, tags=["health"])
def health(settings: settings_dependency) -> HealthResponse:
    return liveness(settings)


@router.post("/analysis/summary", response_model=SummaryResponse, tags=["analysis"])
def summary(request: RecordSetRequest, settings: settings_dependency) -> SummaryResponse:
    if len(request.records) > settings.max_records_per_request:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too many records")
    try:
        return SummaryResponse.model_validate(summarize_records(request.records))
    except DataProcessingError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.post("/analysis/sentiment", response_model=SentimentResponse, tags=["analysis"])
def sentiment(request: SentimentRequest, settings: settings_dependency) -> SentimentResponse:
    if len(request.texts) > settings.max_texts_per_request:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too many texts")
    return SentimentResponse.model_validate(sentiment_service.analyze_batch(request.texts))


@router.post("/predictions/anomalies", response_model=AnomalyResponse, tags=["predictions"])
def anomalies(request: AnomalyRequest, settings: settings_dependency) -> AnomalyResponse:
    if len(request.records) > settings.max_records_per_request:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too many records")
    try:
        result = anomaly_service.detect(
            request.records,
            request.contamination or settings.anomaly_contamination,
            request.feature_columns,
        )
        return AnomalyResponse.model_validate(result)
    except DataProcessingError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.post("/predictions/predict", response_model=PredictionResponse, tags=["predictions"])
def predict(request: PredictionRequest, settings: settings_dependency) -> PredictionResponse:
    if len(request.records) > settings.max_records_per_request:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too many records")
    try:
        service = PredictionService(settings.model_artifact_path, settings.model_target_column)
        return PredictionResponse.model_validate(service.predict(request.records))
    except ModelInferenceError as exc:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
