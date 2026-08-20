"""Train and persist a production-style tabular regression pipeline.

The CLI accepts a CSV or, when no input is supplied, creates a deterministic
synthetic fixture useful for demonstrating the end-to-end workflow locally.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from data.preprocessing import build_preprocessor, infer_feature_spec
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

LOGGER = logging.getLogger(__name__)


def build_demo_dataset(n_samples: int, random_state: int) -> pd.DataFrame:
    """Create a deterministic mixed-type regression fixture for local usage."""

    values, target = make_regression(
        n_samples=n_samples,
        n_features=3,
        n_informative=3,
        noise=12.0,
        random_state=random_state,
    )
    frame = pd.DataFrame(values, columns=["engagement", "latency", "usage"])
    frame["segment"] = np.where(frame["engagement"] > 0, "enterprise", "self_serve")
    frame["target"] = target
    return frame


def train(
    input_path: Path | None,
    output_dir: Path,
    target_column: str,
    n_samples: int,
    random_state: int,
) -> dict[str, object]:
    """Train a pipeline and return a serializable training summary."""

    frame = pd.read_csv(input_path) if input_path else build_demo_dataset(n_samples, random_state)
    spec = infer_feature_spec(frame, target_column)
    x_train, x_test, y_train, y_test = train_test_split(
        frame.drop(columns=[target_column]),
        frame[target_column],
        test_size=0.2,
        random_state=random_state,
    )
    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(spec)),
            ("regressor", Ridge(alpha=1.0)),
        ]
    )
    pipeline.fit(x_train, y_train)
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = output_dir / "regression_pipeline.joblib"
    metadata_path = output_dir / "regression_pipeline.metadata.json"
    joblib.dump(pipeline, artifact_path)
    metadata = {
        "artifact": str(artifact_path),
        "target_column": target_column,
        "numeric_features": spec.numeric,
        "categorical_features": spec.categorical,
        "train_rows": len(x_train),
        "test_rows": len(x_test),
        "random_state": random_state,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    LOGGER.info("Persisted model to %s", artifact_path)
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="CSV containing features and the target")
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    parser.add_argument("--target-column", default="target")
    parser.add_argument("--n-samples", type=int, default=1000)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    train(args.input, args.output_dir, args.target_column, args.n_samples, args.random_state)


if __name__ == "__main__":
    main()
