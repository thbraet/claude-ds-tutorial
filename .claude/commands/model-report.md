Generate a comprehensive model evaluation report.

If arguments are provided, focus on: $ARGUMENTS
Otherwise, evaluate all trained models found in the project.

## Report Sections

### 1. Executive Summary
- Best performing model and its key metric
- Business impact translation (what does this metric mean in real terms?)
- Recommendation: deploy, iterate, or abandon

### 2. Model Comparison Table
| Model | RMSLE | MAE | MAPE | Training Time | # Features |
For each model found in the project, calculate metrics on the test set.

### 3. Best Model Deep Dive
- Hyperparameters used
- Feature importance (top 15 features, bar chart)
- Learning curves (training vs validation error over epochs/trees)
- Prediction vs actual scatter plot
- Residual analysis (distribution of errors, errors over time)

### 4. Segment Analysis
- Performance by store (which stores are hardest to predict?)
- Performance by product family (which categories are hardest?)
- Performance by time period (does accuracy degrade for further-out predictions?)

### 5. Error Analysis
- Worst predictions: top 20 biggest misses (what went wrong?)
- Systematic biases: does the model consistently over/under-predict for certain segments?
- Holiday/promotion impact on error rates

### 6. Business Impact
- Translate RMSLE/MAE into: estimated units of overstock, estimated lost sales from out-of-stock
- Compare to the naive baseline (last week's sales)
- Estimated dollar impact using average unit price per family

### 7. Recommendations
- Model selection recommendation with justification
- Next steps for improvement (more features, more data, different algorithm)
- Risks and limitations to communicate to stakeholders

## Output
- Save the report as `reports/model_evaluation_report.md`
- Save all visualizations as PNGs in `reports/figures/`
