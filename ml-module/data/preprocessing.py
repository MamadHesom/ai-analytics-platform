"""Reusable preprocessing utilities for tabular machine-learning workflows."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


@dataclass(frozen=True)
class FeatureSpec:
    """Feature groups selected from a training frame."""

    numeric: list[str]
    categorical: list[str]


def infer_feature_spec(frame: pd.DataFrame, target_column: str) -> FeatureSpec:
    """Infer feature columns while excluding the target and unsupported all-null columns."""

    if target_column not in frame.columns:
        raise ValueError(f"Target column {target_column!r} is not present")
    features = frame.drop(columns=[target_column])
    features = features.dropna(axis=1, how="all")
    numeric = [str(column) for column in features.select_dtypes(include="number").columns]
    categorical = [str(column) for column in features.select_dtypes(exclude="number").columns]
    if not numeric and not categorical:
        raise ValueError("No usable feature columns were found")
    return FeatureSpec(numeric=numeric, categorical=categorical)


def build_preprocessor(spec: FeatureSpec) -> ColumnTransformer:
    """Construct a leakage-safe preprocessing transformer for a mixed-type dataset."""

    transformers: list[tuple[str, Pipeline, list[str]]] = []
    if spec.numeric:
        transformers.append(
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                spec.numeric,
            )
        )
    if spec.categorical:
        transformers.append(
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                    ]
                ),
                spec.categorical,
            )
        )
    return ColumnTransformer(transformers=transformers, remainder="drop", verbose_feature_names_out=False)
