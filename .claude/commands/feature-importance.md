Analyze and visualize feature importance for: $ARGUMENTS

If no arguments provided, analyze the best model found in the project.

## Analysis Steps

### 1. Built-in Feature Importance
- For tree-based models: extract feature_importances_ (gain-based)
- Plot top 20 features as horizontal bar chart

### 2. Permutation Importance
- Run sklearn permutation_importance on the test set
- Compare with built-in importance (discrepancies reveal potential issues)
- Plot top 20 features with error bars

### 3. SHAP Values (if shap is installed)
- Calculate SHAP values for a sample of test data (max 1000 rows for speed)
- SHAP summary plot (beeswarm)
- SHAP dependence plots for top 5 features

### 4. Feature Group Analysis
Group features by category and show aggregate importance:
- Time features (day_of_week, month, etc.)
- Lag features (sales_lag_7d, etc.)
- Rolling features (rolling_mean, rolling_std)
- Promotion features
- Store features
- Product features
- External features (oil price, holidays)

### 5. Interpretation
- Which feature groups drive the model most?
- Are there surprising findings? (e.g., a feature you expected to matter doesn't)
- Are there redundant features that could be removed?
- Business interpretation: what does this tell us about what drives sales?

## Output
- Print a summary table of feature importances to console
- Save visualizations to `reports/figures/`
- Generate a brief markdown summary suitable for stakeholders
