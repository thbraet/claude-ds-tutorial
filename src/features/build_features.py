"""Feature engineering pipeline for the Store Sales Forecasting project.

This module is intentionally minimal — users will build it out WITH Claude
during the Data Preparation tutorial chapter.
"""

import pandas as pd


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add calendar-based time features from the date column."""
    df = df.copy()
    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["day_of_month"] = df["date"].dt.day
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    df["is_month_start"] = df["date"].dt.is_month_start.astype(int)
    df["is_month_end"] = df["date"].dt.is_month_end.astype(int)
    return df


def add_lag_features(
    df: pd.DataFrame,
    group_cols: list[str],
    target_col: str = "sales",
    lags: list[int] | None = None,
) -> pd.DataFrame:
    """Add lag features for a target column, grouped by store and family."""
    df = df.copy()
    lags = lags or [7, 14, 28]
    for lag in lags:
        col_name = f"{target_col}_lag_{lag}d"
        df[col_name] = df.groupby(group_cols)[target_col].shift(lag)
    return df


def add_rolling_features(
    df: pd.DataFrame,
    group_cols: list[str],
    target_col: str = "sales",
    windows: list[int] | None = None,
) -> pd.DataFrame:
    """Add rolling mean and std features, grouped by store and family."""
    df = df.copy()
    windows = windows or [7, 28]
    for window in windows:
        rolled = df.groupby(group_cols)[target_col].transform(
            lambda x: x.shift(1).rolling(window, min_periods=1).mean()
        )
        df[f"{target_col}_rolling_{window}d_mean"] = rolled

        rolled_std = df.groupby(group_cols)[target_col].transform(
            lambda x: x.shift(1).rolling(window, min_periods=1).std()
        )
        df[f"{target_col}_rolling_{window}d_std"] = rolled_std
    return df
