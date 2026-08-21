"""Evaluate persisted models with regression metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from models.train_model import build_demo_dataset


def evaluate(artifact_path: Path, n_samples: int = 1000, random_state: int = 42) -> dict[str, float]:
    """Evaluate a persisted pipeline on a deterministic holdout fixture."""

    model = joblib.load(artifact_path)
    frame = build_demo_dataset(n_samples, random_state)
    features = frame.drop(columns=["target"])
    x_train, x_test, y_train, y_test = train_test_split(
        features, frame["target"], test_size=0.2, random_state=random_state
    )
    # The persisted model was trained with the same deterministic split convention.
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    mse = mean_squared_error(y_test, predictions)
    return {
        "mae": float(mean_absolute_error(y_test, predictions)),
        "rmse": float(mse**0.5),
        "r2": float(r2_score(y_test, predictions)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--n-samples", type=int, default=1000)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    metrics = evaluate(args.artifact, args.n_samples, args.random_state)
    rendered = json.dumps(metrics, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
