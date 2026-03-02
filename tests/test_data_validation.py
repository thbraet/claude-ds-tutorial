"""Tests for the data validation module."""

import pandas as pd
import pytest

from src.data.validate import (
    check_duplicates,
    check_missing_values,
    validate_sales_data,
)


@pytest.fixture
def valid_sales_df():
    """A minimal valid sales DataFrame."""
    return pd.DataFrame({
        "date": pd.to_datetime(["2016-01-01", "2016-01-02", "2016-01-03"]),
        "store_nbr": pd.Categorical([1, 1, 2]),
        "family": pd.Categorical(["GROCERY I", "DAIRY", "BEVERAGES"]),
        "sales": [100.0, 50.5, 200.0],
        "onpromotion": [0, 1, 0],
    })


@pytest.fixture
def invalid_sales_df():
    """A sales DataFrame with various issues."""
    return pd.DataFrame({
        "date": pd.to_datetime(["2016-01-01", "2016-01-02", "2016-01-03"]),
        "store_nbr": pd.Categorical([1, 1, 99]),  # 99 is invalid
        "family": pd.Categorical(["GROCERY I", "UNKNOWN_FAMILY", "DAIRY"]),
        "sales": [100.0, -5.0, 200.0],  # negative sales
        "onpromotion": [0, 1, 0],
    })


def test_validate_valid_data(valid_sales_df):
    issues = validate_sales_data(valid_sales_df)
    assert len(issues) == 0


def test_validate_catches_negative_sales(invalid_sales_df):
    issues = validate_sales_data(invalid_sales_df)
    assert any("negative sales" in issue for issue in issues)


def test_validate_catches_invalid_stores(invalid_sales_df):
    issues = validate_sales_data(invalid_sales_df)
    assert any("invalid store" in issue for issue in issues)


def test_validate_catches_unknown_families(invalid_sales_df):
    issues = validate_sales_data(invalid_sales_df)
    assert any("Unknown product families" in issue for issue in issues)


def test_check_missing_values():
    df = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, 6], "c": [None, None, 9]})
    report = check_missing_values(df, threshold=0.05)
    assert "c" in report.index
    assert report.loc["c", "missing_count"] == 2


def test_check_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 4]})
    assert check_duplicates(df) == 1
    assert check_duplicates(df, key_columns=["a"]) == 1
