Run a comprehensive data quality assessment on: $ARGUMENTS

If no path is provided, check all files in `data/raw/` and `data/processed/`.

## Quality Dimensions

Check each of these dimensions systematically:

### 1. Completeness
- Missing values per column (count, percentage)
- Rows with ANY missing value
- Columns with >5% missing (flag as warning), >20% missing (flag as critical)

### 2. Uniqueness
- Duplicate rows (exact matches)
- Near-duplicates (same key columns but different values)
- Expected primary key uniqueness check

### 3. Validity
- Values within expected ranges (refer to data-validation skill rules)
- Data type correctness (dates as datetime, categoricals as category)
- Format consistency (date formats, string patterns)

### 4. Consistency
- Cross-column logic checks (e.g., sales >= 0 when transactions > 0)
- Cross-file consistency if multiple related files exist
- Referential integrity between tables (store IDs match, family names match)

### 5. Timeliness
- Date range of the data
- Any gaps in the time series
- Most recent data point

## Output Format

Produce a structured markdown report following the template in the data-validation skill. Include a severity rating for each finding:
- **CRITICAL**: Must fix before any analysis (data leakage, wrong types, major missing data)
- **WARNING**: Should investigate (moderate missing data, suspicious outliers)
- **INFO**: Worth noting (minor patterns, optimization opportunities)

End with a prioritized action list of recommended fixes.
