---
name: crisp-dm-guide
description: "CRISP-DM methodology guide for data science projects. Activates when discussing project phases, planning analysis workflows, or when the user mentions business understanding, data understanding, data preparation, modeling, evaluation, or deployment in a data science context."
---

# CRISP-DM Methodology Guide

## Instructions

When working on a data science task, identify which CRISP-DM phase applies and guide the user accordingly.

### Phase Detection

Analyze the user's request and map it to one of these phases:

1. **Business Understanding** — if the user discusses goals, KPIs, stakeholders, problem definition, success criteria, project scope, or business requirements
2. **Data Understanding** — if the user explores datasets, runs EDA, checks data quality, describes variables, or investigates distributions
3. **Data Preparation** — if the user cleans data, handles missing values, engineers features, transforms variables, merges datasets, or encodes categoricals
4. **Modeling** — if the user selects algorithms, trains models, tunes hyperparameters, runs cross-validation, or compares model architectures
5. **Evaluation** — if the user assesses model performance, calculates business impact, checks for bias/leakage, compares to baselines, or prepares recommendations
6. **Deployment** — if the user packages models, creates APIs, sets up monitoring, writes documentation, or plans maintenance

### Phase-Specific Guidance

For each phase, ensure these deliverables are addressed:

**Business Understanding deliverables:**
- Business objectives document with measurable success criteria
- Data mining goals mapped to business goals
- Project plan with resources, risks, and timeline
- Stakeholder map with data owners identified

**Data Understanding deliverables:**
- Data dictionary describing every variable
- Data quality report (missing values, outliers, duplicates, type mismatches)
- Initial statistical summary (distributions, correlations, key patterns)
- Visualization of key relationships

**Data Preparation deliverables:**
- Documented data cleaning steps (reproducible pipeline)
- Feature engineering rationale for each new feature
- Train/validation/test split strategy documented
- Data validation checks that run automatically

**Modeling deliverables:**
- Justification for algorithm selection (why this model for this problem)
- Baseline model results for comparison
- Hyperparameter search strategy and results
- Model artifacts saved in a reproducible format

**Evaluation deliverables:**
- Technical metrics (RMSE, MAE, R², etc.) with confidence intervals
- Business impact translation (metrics → dollars/units/percentage)
- Error analysis (where does the model fail and why)
- Recommendation document for stakeholders

**Deployment deliverables:**
- Prediction API or batch scoring pipeline
- Monitoring plan (data drift, model performance degradation)
- Documentation for maintenance team
- Rollback strategy

### Cross-Phase Reminders

- Always document assumptions and decisions
- Each phase may require revisiting earlier phases (CRISP-DM is iterative)
- Flag when a finding in one phase impacts decisions made in another
- Suggest the user update CLAUDE.md with new project learnings after each phase
