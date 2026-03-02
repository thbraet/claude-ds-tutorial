"""Model training utilities for the Store Sales Forecasting project.

This module provides the basic training scaffold. Users will extend it
with more models during the Modeling tutorial chapter.
"""

from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit


def rmsle(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root Mean Squared Logarithmic Error — the primary evaluation metric."""
    y_pred = np.clip(y_pred, 0, None)  # Predictions must be non-negative
    return np.sqrt(np.mean((np.log1p(y_pred) - np.log1p(y_true)) ** 2))


def time_series_cv_split(
    df: pd.DataFrame,
    n_splits: int = 5,
    test_days: int = 28,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Create time-based cross-validation splits.

    Each fold uses a 28-day test window, expanding the training window.
    """
    dates = df["date"].sort_values().unique()
    splits = []

    for i in range(n_splits):
        test_end_idx = len(dates) - i * test_days
        test_start_idx = test_end_idx - test_days

        if test_start_idx <= 0:
            break

        test_dates = dates[test_start_idx:test_end_idx]
        train_dates = dates[:test_start_idx]

        train_idx = df[df["date"].isin(train_dates)].index.values
        test_idx = df[df["date"].isin(test_dates)].index.values

        splits.append((train_idx, test_idx))

    return splits


def create_experiment_log(
    model_name: str,
    params: dict,
    metrics: dict,
    feature_count: int,
    notes: str = "",
) -> dict:
    """Create a structured experiment log entry."""
    return {
        "timestamp": datetime.now().isoformat(),
        "model": model_name,
        "params": params,
        "metrics": metrics,
        "feature_count": feature_count,
        "notes": notes,
    }
