# Store Sales Forecasting — CRISP-DM Tutorial Project

## Project Overview

This is a retail store sales forecasting project following the CRISP-DM methodology.
It doubles as a hands-on tutorial teaching data scientists how to use Claude Code effectively.

**Dataset**: Kaggle "Store Sales — Time Series Forecasting" (Ecuadorian grocery retail).

## Business Context

**Client**: Favorita — Ecuadorian grocery retail chain
**Stores**: 54 locations across Ecuador
**Product families**: 33 categories (Grocery, Produce, Dairy, Bakery, Meats, etc.)
**Historical data**: 2013-01-01 to 2017-08-15

### Business Targets
- Reduce overstock waste: 15% (shrinkage from 2.8% → 2.38%)
- Reduce out-of-stock incidents: 20% (OOS from 6.5% → 5.2%)
- Estimated annual savings: $2.5M

## Forecast Requirements

- **Target variable**: Daily unit sales
- **Granularity**: Store × Product Family × Date
- **Prediction horizon**: 16 days ahead
- **Output**: Point forecast + 80% prediction interval
- **Baseline**: Naive seasonal (same day last week)

## Model Success Criteria

| Metric | Target | Purpose |
|--------|--------|---------|
| WMAPE | <15% | Primary metric (weighted by volume) |
| RMSE | <50 units/day | Penalizes large errors |
| MAE | <30 units/day | Interpretable |
| Bias | ±5% | No systematic over/under-forecast |

## Domain Rules

- Ecuador's economy is oil-dependent — oil price is a valid feature
- Holidays vary by region (national, regional, local, transferred)
- Perishables (Produce, Dairy, Bakery, Meats) have different dynamics
- Promotions can cause demand spikes of 3-5x normal sales
- Store "transfers" in the data are inter-store movements, not customer sales

## Key Documents

- `docs/project-charter.md` — Full business requirements and stakeholder map
- `docs/data_dictionary.md` — Column definitions and data sources (TODO)
- `notebooks/01_eda.ipynb` — Exploratory analysis (TODO)

## Tech Stack

- Python 3.11+
- pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn
- DuckDB for SQL-based data exploration
- Jupyter notebooks for interactive analysis
- pytest for testing
- FastAPI for model serving (deployment phase)

## Conventions

- Use snake_case for all Python identifiers
- Store raw data in `data/raw/`, processed data in `data/processed/`
- Never commit data files larger than 50MB to git
- Always use parquet for processed data (not CSV or pickle)
- All notebooks must have markdown headers explaining each section
- Write docstrings for all public functions in src/
- Type hints on all function signatures

## Project Structure

- `tutorial/` — Step-by-step tutorial chapters (00 through 08)
- `data/` — Raw, processed, and external datasets
- `notebooks/` — Jupyter notebooks for interactive analysis
- `src/` — Reusable Python modules (data loading, features, models, visualization)
- `tests/` — pytest test suite
- `.claude/` — Claude Code configuration (agents, skills, commands, hooks)

## How to Run

```bash
pip install -r requirements.txt
python -m pytest tests/
jupyter lab notebooks/
```

## CRISP-DM Phase Tracking

When working on this project, identify which CRISP-DM phase applies:
1. Business Understanding — problem definition, goals, success criteria
2. Data Understanding — EDA, data quality, initial insights
3. Data Preparation — cleaning, feature engineering, transformations
4. Modeling — algorithm selection, training, hyperparameter tuning
5. Evaluation — metrics, business impact, model comparison
6. Deployment — API creation, monitoring, documentation
