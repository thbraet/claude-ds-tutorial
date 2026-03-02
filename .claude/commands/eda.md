Perform a comprehensive Exploratory Data Analysis on the dataset at path: $ARGUMENTS

If no path is provided, analyze all CSV files in `data/raw/`.

## Steps

1. **Load the data** and report the shape (rows x columns)
2. **Data types**: List each column with its dtype and sample values
3. **Missing values**: Count and percentage per column, visualize the pattern
4. **Descriptive statistics**: mean, median, std, min, max, quartiles for all numeric columns
5. **Distribution analysis**: Plot histograms for numeric columns, value counts for categoricals
6. **Correlation matrix**: Heatmap of numeric column correlations
7. **Time patterns** (if date column exists): Plot trends, seasonality, day-of-week effects
8. **Outlier detection**: Flag values beyond 3 standard deviations or IQR method
9. **Key findings**: Summarize the 5 most important observations about this data

## Output

- Print all statistics and findings to the console
- Save visualizations as PNG files in `notebooks/figures/`
- Generate a summary markdown section that can be pasted into a notebook

## Important

- Use matplotlib and seaborn for visualizations
- Set figure sizes to (12, 6) for readability
- Always label axes and add titles to plots
- Use the data-validation skill to validate data quality alongside the EDA
