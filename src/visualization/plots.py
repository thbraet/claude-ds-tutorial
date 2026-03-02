"""Visualization utilities for the Store Sales Forecasting project.

Provides consistent, publication-quality plots for EDA and model evaluation.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Project-wide plot style
FIGSIZE = (12, 6)
PALETTE = "Set2"
plt.style.use("seaborn-v0_8-whitegrid")


def save_fig(fig: plt.Figure, filename: str, output_dir: str = "notebooks/figures") -> Path:
    """Save a figure to the output directory."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    filepath = output_path / filename
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return filepath


def plot_sales_over_time(
    df: pd.DataFrame,
    date_col: str = "date",
    sales_col: str = "sales",
    title: str = "Total Sales Over Time",
) -> plt.Figure:
    """Plot aggregated daily sales as a time series."""
    daily_sales = df.groupby(date_col)[sales_col].sum()
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(daily_sales.index, daily_sales.values, linewidth=0.8)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Sales")
    return fig


def plot_sales_by_family(
    df: pd.DataFrame,
    top_n: int = 15,
    title: str = "Total Sales by Product Family",
) -> plt.Figure:
    """Horizontal bar chart of total sales per product family."""
    family_sales = df.groupby("family")["sales"].sum().sort_values(ascending=True).tail(top_n)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    family_sales.plot(kind="barh", ax=ax, color=sns.color_palette(PALETTE, top_n))
    ax.set_title(title)
    ax.set_xlabel("Total Sales")
    return fig


def plot_missing_values(df: pd.DataFrame, title: str = "Missing Values") -> plt.Figure:
    """Heatmap showing missing value patterns."""
    fig, ax = plt.subplots(figsize=FIGSIZE)
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if len(missing) == 0:
        ax.text(0.5, 0.5, "No missing values found", ha="center", va="center", fontsize=14)
    else:
        missing_pct = missing / len(df) * 100
        missing_pct.plot(kind="barh", ax=ax, color="salmon")
        ax.set_title(title)
        ax.set_xlabel("Missing %")
    return fig


def plot_predictions_vs_actual(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "Predicted vs Actual Sales",
) -> plt.Figure:
    """Scatter plot comparing predictions to actual values."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(y_true, y_pred, alpha=0.3, s=5)
    max_val = max(y_true.max(), y_pred.max())
    ax.plot([0, max_val], [0, max_val], "r--", linewidth=1, label="Perfect prediction")
    ax.set_title(title)
    ax.set_xlabel("Actual Sales")
    ax.set_ylabel("Predicted Sales")
    ax.legend()
    return fig
