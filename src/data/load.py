"""Data loading utilities for the Store Sales Forecasting project."""

from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).parent.parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"


def load_train(path: Path | None = None) -> pd.DataFrame:
    """Load the training sales data."""
    path = path or RAW_DIR / "train.csv"
    df = pd.read_csv(path, parse_dates=["date"])
    df["store_nbr"] = df["store_nbr"].astype("category")
    df["family"] = df["family"].astype("category")
    return df


def load_test(path: Path | None = None) -> pd.DataFrame:
    """Load the test data for predictions."""
    path = path or RAW_DIR / "test.csv"
    df = pd.read_csv(path, parse_dates=["date"])
    df["store_nbr"] = df["store_nbr"].astype("category")
    df["family"] = df["family"].astype("category")
    return df


def load_stores(path: Path | None = None) -> pd.DataFrame:
    """Load store metadata (city, state, type, cluster)."""
    path = path or RAW_DIR / "stores.csv"
    return pd.read_csv(path)


def load_oil(path: Path | None = None) -> pd.DataFrame:
    """Load daily oil prices (external economic indicator)."""
    path = path or RAW_DIR / "oil.csv"
    df = pd.read_csv(path, parse_dates=["date"])
    df.rename(columns={"dcoilwtico": "oil_price"}, inplace=True)
    return df


def load_holidays(path: Path | None = None) -> pd.DataFrame:
    """Load holiday and events calendar."""
    path = path or RAW_DIR / "holidays_events.csv"
    return pd.read_csv(path, parse_dates=["date"])


def load_transactions(path: Path | None = None) -> pd.DataFrame:
    """Load daily transaction counts per store."""
    path = path or RAW_DIR / "transactions.csv"
    return pd.read_csv(path, parse_dates=["date"])


def load_all_raw() -> dict[str, pd.DataFrame]:
    """Load all raw datasets and return as a dictionary."""
    return {
        "train": load_train(),
        "test": load_test(),
        "stores": load_stores(),
        "oil": load_oil(),
        "holidays": load_holidays(),
        "transactions": load_transactions(),
    }
