"""Prediction pipeline for the Store Sales Forecasting project.

This module is intentionally minimal — users will build the full prediction
pipeline during the Deployment tutorial chapter.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd


def load_model(model_path: str | Path):
    """Load a trained model from disk."""
    return joblib.load(model_path)


def predict(model, features: pd.DataFrame) -> np.ndarray:
    """Generate predictions, clipping to non-negative values."""
    predictions = model.predict(features)
    return np.clip(predictions, 0, None)


def format_submission(
    test_df: pd.DataFrame,
    predictions: np.ndarray,
    id_col: str = "id",
    target_col: str = "sales",
) -> pd.DataFrame:
    """Format predictions into a submission-ready DataFrame."""
    submission = pd.DataFrame({
        id_col: test_df[id_col],
        target_col: predictions,
    })
    return submission
