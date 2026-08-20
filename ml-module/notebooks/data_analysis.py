"""Exploratory data analysis workflow usable as a script or notebook source.

Run with ``python data_analysis.py --input data.csv --output-dir reports``.
The functions return ordinary Python objects so they can be imported into a
Jupyter notebook without depending on hidden global state.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def profile(frame: pd.DataFrame) -> dict[str, object]:
    """Return compact structural and data-quality findings."""

    return {
        "shape": {"rows": int(frame.shape[0]), "columns": int(frame.shape[1])},
        "dtypes": {str(column): str(dtype) for column, dtype in frame.dtypes.items()},
        "missing_values": {str(column): int(value) for column, value in frame.isna().sum().items()},
        "duplicate_rows": int(frame.duplicated().sum()),
        "numeric_describe": frame.describe(include="number").round(4).to_dict(),
    }


def create_plots(frame: pd.DataFrame, output_dir: Path) -> list[Path]:
    """Save distribution and correlation plots for numeric columns."""

    output_dir.mkdir(parents=True, exist_ok=True)
    numeric = frame.select_dtypes(include="number")
    outputs: list[Path] = []
    if numeric.empty:
        return outputs

    for column in numeric.columns:
        path = output_dir / f"distribution_{column}.png"
        plt.figure(figsize=(8, 4.5))
        sns.histplot(numeric[column].dropna(), kde=True)
        plt.title(f"Distribution of {column}")
        plt.tight_layout()
        plt.savefig(path, dpi=150)
        plt.close()
        outputs.append(path)

    if len(numeric.columns) > 1:
        path = output_dir / "correlation_heatmap.png"
        plt.figure(figsize=(8, 6))
        sns.heatmap(numeric.corr(), annot=True, fmt=".2f", cmap="vlag", center=0)
        plt.title("Numeric Feature Correlations")
        plt.tight_layout()
        plt.savefig(path, dpi=150)
        plt.close()
        outputs.append(path)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    frame = pd.read_csv(args.input)
    print(profile(frame))
    for path in create_plots(frame, args.output_dir):
        print(path)


if __name__ == "__main__":
    main()
