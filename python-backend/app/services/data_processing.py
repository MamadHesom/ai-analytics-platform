"""Business logic for tabular data validation and descriptive analytics."""

from typing import Any

import pandas as pd


class DataProcessingError(ValueError):
    """Raised when records cannot be transformed into an analyzable table."""


def records_to_frame(records: list[dict[str, Any]]) -> pd.DataFrame:
    """Convert records to a normalized DataFrame with defensive validation."""

    if not records:
        raise DataProcessingError("At least one record is required")
    frame = pd.DataFrame.from_records(records)
    if frame.empty or frame.shape[1] == 0:
        raise DataProcessingError("Records do not contain usable columns")
    return frame


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Produce JSON-serializable descriptive statistics for mixed-type records."""

    frame = records_to_frame(records)
    numeric = frame.select_dtypes(include="number")
    numeric_summary: dict[str, dict[str, float | int | None]] = {}
    if not numeric.empty:
        summary = numeric.describe().transpose()
        for column, row in summary.iterrows():
            numeric_summary[str(column)] = {
                key: (None if pd.isna(value) else float(value)) for key, value in row.to_dict().items()
            }

    return {
        "rows": int(len(frame)),
        "columns": [str(column) for column in frame.columns],
        "numeric_summary": numeric_summary,
        "missing_values": {str(column): int(value) for column, value in frame.isna().sum().items()},
        "categorical_cardinality": {
            str(column): int(frame[column].nunique(dropna=True))
            for column in frame.select_dtypes(exclude="number").columns
        },
    }


def numeric_features(records: list[dict[str, Any]], columns: list[str] | None = None) -> tuple[pd.DataFrame, list[str]]:
    """Return finite numeric features with median imputation for inference."""

    frame = records_to_frame(records)
    selected = columns or [str(column) for column in frame.select_dtypes(include="number").columns]
    if not selected:
        raise DataProcessingError("At least one numeric feature is required")
    missing = sorted(set(selected) - set(frame.columns))
    if missing:
        raise DataProcessingError(f"Unknown feature columns: {', '.join(missing)}")
    features = frame[selected].apply(pd.to_numeric, errors="coerce")
    features = features.replace([float("inf"), float("-inf")], pd.NA)
    features = features.fillna(features.median(numeric_only=True)).fillna(0.0)
    return features.astype(float), selected
