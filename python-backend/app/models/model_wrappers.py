"""Reusable model wrappers kept separate from HTTP and business orchestration code."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd


class PersistedModel:
    """Lazy-loading wrapper around a joblib-compatible scikit-learn estimator."""

    def __init__(self, artifact_path: str | Path) -> None:
        self.artifact_path = Path(artifact_path)
        self._estimator: Any | None = None

    def load(self) -> Any:
        if self._estimator is None:
            if not self.artifact_path.is_file():
                raise FileNotFoundError(f"Model artifact does not exist: {self.artifact_path}")
            self._estimator = joblib.load(self.artifact_path)
        return self._estimator

    def predict(self, records: list[dict[str, Any]]) -> list[float]:
        frame = pd.DataFrame.from_records(records)
        values = self.load().predict(frame)
        return [float(value) for value in values]

    @property
    def loaded(self) -> bool:
        return self._estimator is not None
