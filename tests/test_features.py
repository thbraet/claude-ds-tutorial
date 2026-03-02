"""Tests for the feature engineering module."""

import pandas as pd
import pytest

from src.features.build_features import (
    add_lag_features,
    add_rolling_features,
    add_time_features,
)


@pytest.fixture
def sample_df():
    """Sample DataFrame for feature engineering tests."""
    dates = pd.date_range("2016-01-01", periods=30, freq="D")
    return pd.DataFrame({
        "date": dates,
        "store_nbr": [1] * 30,
        "family": ["GROCERY I"] * 30,
        "sales": list(range(100, 130)),
    })


def test_add_time_features(sample_df):
    result = add_time_features(sample_df)
    assert "day_of_week" in result.columns
    assert "month" in result.columns
    assert "is_weekend" in result.columns
    assert result["day_of_week"].between(0, 6).all()
    assert result["is_weekend"].isin([0, 1]).all()


def test_add_lag_features(sample_df):
    result = add_lag_features(sample_df, group_cols=["store_nbr", "family"], lags=[7])
    assert "sales_lag_7d" in result.columns
    # First 7 days should be NaN (no data to lag from)
    assert result["sales_lag_7d"].isna().sum() == 7
    # Day 8 should equal day 1's value
    assert result["sales_lag_7d"].iloc[7] == 100.0


def test_add_rolling_features(sample_df):
    result = add_rolling_features(
        sample_df, group_cols=["store_nbr", "family"], windows=[7]
    )
    assert "sales_rolling_7d_mean" in result.columns
    assert "sales_rolling_7d_std" in result.columns


def test_time_features_dont_modify_original(sample_df):
    original_cols = set(sample_df.columns)
    add_time_features(sample_df)
    assert set(sample_df.columns) == original_cols
