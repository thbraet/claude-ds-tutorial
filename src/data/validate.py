"""Data validation functions for the Store Sales Forecasting project."""

import pandas as pd

EXPECTED_FAMILIES = [
    "AUTOMOTIVE", "BABY CARE", "BEAUTY", "BEVERAGES", "BOOKS",
    "BREAD/BAKERY", "CELEBRATION", "CLEANING", "DAIRY", "DELI",
    "EGGS", "FROZEN FOODS", "GROCERY I", "GROCERY II", "HARDWARE",
    "HOME AND KITCHEN", "HOME APPLIANCES", "HOME CARE", "LADIESWEAR",
    "LAWN AND GARDEN", "LINGERIE", "LIQUOR,WINE,BEER", "MAGAZINES",
    "MEATS", "PERSONAL CARE", "PET SUPPLIES", "PLAYERS AND ELECTRONICS",
    "POULTRY", "PREPARED FOODS", "PRODUCE", "SCHOOL AND OFFICE SUPPLIES",
    "SEAFOOD",
]


def validate_sales_data(df: pd.DataFrame) -> list[str]:
    """Validate the sales training/test data. Returns a list of issues found."""
    issues = []

    # Check required columns
    required_cols = {"date", "store_nbr", "family", "sales"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        issues.append(f"Missing required columns: {missing_cols}")
        return issues  # Can't validate further without required columns

    # Check for nulls in critical columns
    for col in ["date", "store_nbr", "family"]:
        null_count = df[col].isna().sum()
        if null_count > 0:
            issues.append(f"Column '{col}' has {null_count} null values")

    # Check sales non-negative
    if "sales" in df.columns:
        negative_sales = (df["sales"] < 0).sum()
        if negative_sales > 0:
            issues.append(f"Found {negative_sales} rows with negative sales")

    # Check store numbers in valid range
    if "store_nbr" in df.columns:
        invalid_stores = df[~df["store_nbr"].astype(int).between(1, 54)]
        if len(invalid_stores) > 0:
            issues.append(f"Found {len(invalid_stores)} rows with invalid store numbers")

    # Check product families
    if "family" in df.columns:
        unknown_families = set(df["family"].unique()) - set(EXPECTED_FAMILIES)
        if unknown_families:
            issues.append(f"Unknown product families: {unknown_families}")

    # Check date range
    if "date" in df.columns:
        min_date = df["date"].min()
        max_date = df["date"].max()
        if min_date < pd.Timestamp("2013-01-01"):
            issues.append(f"Dates before expected range: {min_date}")
        if max_date > pd.Timestamp("2017-12-31"):
            issues.append(f"Dates after expected range: {max_date}")

    return issues


def check_missing_values(df: pd.DataFrame, threshold: float = 0.05) -> pd.DataFrame:
    """Report columns with missing values above threshold."""
    missing = df.isna().sum()
    missing_pct = missing / len(df)
    report = pd.DataFrame({
        "missing_count": missing,
        "missing_pct": missing_pct,
        "above_threshold": missing_pct > threshold,
    })
    return report[report["missing_count"] > 0].sort_values("missing_pct", ascending=False)


def check_duplicates(df: pd.DataFrame, key_columns: list[str] | None = None) -> int:
    """Count duplicate rows, optionally by key columns."""
    if key_columns:
        return df.duplicated(subset=key_columns).sum()
    return df.duplicated().sum()
