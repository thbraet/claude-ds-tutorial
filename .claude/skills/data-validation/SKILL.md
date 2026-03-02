---
name: data-validation
description: "Data quality and validation patterns for data science pipelines. Activates when loading data files, checking data quality, validating dataframes, or when data integrity issues are detected."
---

# Data Validation Skill

## Instructions

Apply data quality checks proactively whenever working with data loading, transformation, or storage.

### Automatic Checks on Data Load

When reading any CSV, Parquet, or database table, always report:

1. **Shape**: rows x columns
2. **Missing values**: count and percentage per column, flag any column with >5% missing
3. **Duplicates**: exact duplicate rows count
4. **Data types**: verify types match expectations (dates as datetime, not strings; IDs as categorical, not numeric)
5. **Value ranges**: min/max for numeric columns — flag obvious outliers (e.g., negative sales, future dates)

### Validation Rules for This Project

Apply these rules specific to the store sales dataset:

```
- date: must be a valid date, no nulls, range 2013-01-01 to 2017-08-15
- store_nbr: integer 1-54, no nulls
- family: must be one of the 33 known product families, no nulls
- sales: float >= 0, no nulls (zero is valid, negative is not)
- onpromotion: integer >= 0, no nulls
- oil_price (dcoilwtico): float, nulls expected on weekends/holidays
- transactions: integer > 0, nulls expected for some store-dates
```

### Data Quality Report Template

When asked for a data quality check, produce a structured report:

```markdown
## Data Quality Report — [filename]

**Generated**: [date]
**Shape**: [rows] rows x [cols] columns

### Completeness
| Column | Non-null | Missing | Missing % |
|--------|----------|---------|-----------|
| ...    | ...      | ...     | ...       |

### Uniqueness
- Duplicate rows: [count]
- Expected unique key: [columns] — Unique: [yes/no]

### Validity
- Out-of-range values: [list any violations]
- Type mismatches: [list any]

### Consistency
- Cross-column checks: [e.g., sales > 0 when transactions > 0]

### Recommendations
- [Actionable steps to fix identified issues]
```

### Validation on Data Write

When writing processed data files:
- Verify no accidental data loss (output rows should match expected count)
- Confirm output format is parquet (per project conventions)
- Validate column names are snake_case
- Check that no PII or sensitive columns were accidentally included

### Personalization Note

To adapt these validation rules for YOUR data:
- Replace the column-specific rules with your schema expectations
- Add business rules (e.g., "revenue must equal quantity * unit_price")
- Add cross-table consistency checks if working with multiple related tables
- Include data freshness checks ("latest date should be within 24h of today")
