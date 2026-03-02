# Store Sales Forecasting — CRISP-DM Tutorial

A hands-on tutorial teaching data scientists how to use Claude Code effectively through a real-world retail sales forecasting project.

## Overview

This project follows the **CRISP-DM methodology** to build a sales forecasting system for Favorita, an Ecuadorian grocery retail chain. It uses the [Kaggle Store Sales — Time Series Forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting) dataset.

**What you'll learn:**
- How to leverage Claude Code for data science workflows
- CRISP-DM methodology in practice
- Feature engineering for time series forecasting
- Model evaluation and business impact assessment

## Business Context

| Metric | Details |
|--------|---------|
| Client | Favorita (Ecuadorian grocery chain) |
| Stores | 54 locations across Ecuador |
| Products | 33 product families |
| Data Range | 2013-01-01 to 2017-08-15 |
| Forecast Horizon | 16 days ahead |

### Business Targets
- Reduce overstock waste by 15%
- Reduce out-of-stock incidents by 20%
- Estimated annual savings: $2.5M

## Project Structure

```
├── tutorial/           # Step-by-step tutorial chapters (00-08)
├── data/
│   ├── raw/           # Original dataset files
│   ├── processed/     # Cleaned and transformed data
│   └── external/      # External data sources (oil prices, holidays)
├── notebooks/         # Jupyter notebooks for analysis
├── src/
│   ├── data/          # Data loading and validation
│   ├── features/      # Feature engineering
│   ├── models/        # Model training and prediction
│   └── visualization/ # Plotting utilities
├── tests/             # pytest test suite
├── docs/              # Project documentation
└── .claude/           # Claude Code configuration
```

## Tutorial Chapters

| Chapter | Topic | CRISP-DM Phase |
|---------|-------|----------------|
| 00 | Getting Started | Setup |
| 01 | Business Understanding | Business Understanding |
| 02 | Data Understanding | Data Understanding |
| 03 | Data Preparation | Data Preparation |
| 04 | Modeling | Modeling |
| 05 | Evaluation | Evaluation |
| 06 | Deployment | Deployment |
| 07 | Personalization | Advanced |
| 08 | Advanced Patterns | Advanced |

## Getting Started

### Prerequisites
- Python 3.11+
- Claude Code CLI

### Installation

```bash
# Clone the repository
git clone https://github.com/thbraet/claude-ds-tutorial.git
cd claude-ds-tutorial

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download the dataset from Kaggle
# Place files in data/raw/
```

### Running the Project

```bash
# Run tests
python -m pytest tests/

# Start Jupyter Lab
jupyter lab notebooks/
```

## Tech Stack

- **Data Processing**: pandas, numpy, DuckDB
- **Machine Learning**: scikit-learn, XGBoost
- **Visualization**: matplotlib, seaborn
- **Testing**: pytest
- **Deployment**: FastAPI

## Model Success Criteria

| Metric | Target |
|--------|--------|
| WMAPE | < 15% |
| RMSE | < 50 units/day |
| MAE | < 30 units/day |
| Bias | ± 5% |

## License

This project is for educational purposes.

## Acknowledgments

- Dataset: [Kaggle Store Sales Competition](https://www.kaggle.com/competitions/store-sales-time-series-forecasting)
- Methodology: [CRISP-DM](https://en.wikipedia.org/wiki/Cross-industry_standard_process_for_data_mining)
