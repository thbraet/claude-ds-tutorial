"""Tests for the model training utilities."""

import numpy as np
import pandas as pd
import pytest

from src.models.train import create_experiment_log, rmsle, time_series_cv_split


def test_rmsle_perfect_prediction():
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([1.0, 2.0, 3.0])
    assert rmsle(y_true, y_pred) == pytest.approx(0.0)


def test_rmsle_clips_negative_predictions():
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([-1.0, 2.0, 3.0])  # Negative prediction clipped to 0
    result = rmsle(y_true, y_pred)
    assert result > 0
    assert np.isfinite(result)


def test_rmsle_zero_values():
    y_true = np.array([0.0, 0.0, 0.0])
    y_pred = np.array([0.0, 0.0, 0.0])
    assert rmsle(y_true, y_pred) == pytest.approx(0.0)


def test_time_series_cv_split():
    dates = pd.date_range("2016-01-01", periods=180, freq="D")
    df = pd.DataFrame({"date": dates, "value": range(180)})
    splits = time_series_cv_split(df, n_splits=3, test_days=28)

    assert len(splits) == 3
    for train_idx, test_idx in splits:
        # Test set should be 28 days
        assert len(test_idx) == 28
        # Train dates should all be before test dates
        train_dates = df.loc[train_idx, "date"]
        test_dates = df.loc[test_idx, "date"]
        assert train_dates.max() < test_dates.min()


def test_create_experiment_log():
    log = create_experiment_log(
        model_name="XGBoost",
        params={"n_estimators": 100},
        metrics={"rmsle": 0.5},
        feature_count=20,
        notes="baseline run",
    )
    assert log["model"] == "XGBoost"
    assert "timestamp" in log
    assert log["feature_count"] == 20
