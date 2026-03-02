# Project Charter: Favorita Store Sales Forecasting

**Project ID:** FAVORITA-FORECAST-2026
**Date:** March 1, 2026
**Version:** 1.0
**CRISP-DM Phase:** Business Understanding

---

## Executive Summary

Favorita grocery chain is implementing a machine learning-based sales forecasting system to optimize inventory management across 54 stores and 33 product families. By accurately predicting daily sales at the store-product family level, the project aims to reduce overstock waste by 15% and out-of-stock incidents by 20%, translating to estimated annual savings of $2.5M and improved customer satisfaction.

This project will leverage 4+ years of historical sales data (2013-2017) to build predictive models that inform automated replenishment decisions, enabling store managers to stock the right products in the right quantities at the right time.

---

## 1. Business Objectives and Success Criteria

### Primary Business Objectives

1. **Reduce Waste**: Decrease overstock waste by 15% through improved demand prediction
   - Baseline: Current shrinkage rate is 2.8% of total sales
   - Target: Reduce shrinkage to 2.38% (15% reduction)
   - Primary impact on perishable categories (Produce, Dairy, Bakery, Meats)

2. **Improve Availability**: Reduce out-of-stock incidents by 20%
   - Baseline: Current OOS rate is 6.5% across all product families
   - Target: Reduce OOS rate to 5.2% (20% reduction)
   - Focus on high-velocity items and promotional periods

3. **Optimize Inventory Investment**: Maintain or reduce average inventory levels while hitting waste and OOS targets
   - Secondary benefit: Improved cash flow and reduced storage costs

### Success Criteria (Business KPIs)

| Metric | Baseline | Target | Measurement Period |
|--------|----------|--------|-------------------|
| Shrinkage Rate | 2.8% | 2.38% | Monthly average over 6 months post-deployment |
| Out-of-Stock Rate | 6.5% | 5.2% | Weekly average over 6 months post-deployment |
| Stock Turnover (Perishables) | 12x/year | 14x/year | Quarterly average |
| Forecast Accuracy (MAPE) | N/A | <20% | Evaluated on 30-day holdout |
| Cost Savings | $0 | $2.5M/year | Annual run-rate after 6 months |

### Business Value

- **Direct savings**: $1.8M/year from reduced waste (15% reduction in shrinkage)
- **Revenue protection**: $700K/year from reduced lost sales (20% fewer OOS incidents)
- **Customer satisfaction**: Improved availability drives loyalty and basket size
- **Operational efficiency**: Automated replenishment reduces manual forecasting effort

---

## 2. Data Mining Goals

### What We're Predicting

**Target Variable:** Daily unit sales per product family per store
**Granularity:** Store ID × Product Family × Date
**Prediction Horizon:** 16 days ahead (matching typical ordering lead time)
**Output Format:** Point forecast + 80% prediction interval

### Modeling Approach

- **Primary model type:** Time series regression with engineered features
- **Candidate algorithms:** XGBoost, LightGBM, Prophet, SARIMA ensemble
- **Modeling strategy:** Hierarchical forecasting (global model with store/product embeddings)
- **Baseline for comparison:** Naive seasonal forecast (same day last week × trend adjustment)

### Technical Success Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| RMSE (Root Mean Squared Error) | <50 units/day | Penalizes large errors heavily |
| MAE (Mean Absolute Error) | <30 units/day | Interpretable in business terms |
| MAPE (Mean Absolute % Error) | <20% | Industry standard for retail forecasting |
| WMAPE (Weighted MAPE) | <15% | Weighted by sales volume |
| Forecast Bias | Within ±5% | Ensures no systematic over/under-forecasting |

**Evaluation Strategy:**
- Time-based train/validation/test split (no random splits for time series)
- Rolling window backtesting on last 6 months of data
- Separate metrics reported by:
  - Product family (to identify which categories are hardest to forecast)
  - Store type (urban/suburban/rural)
  - Day of week (weekends vs weekdays)
  - Promotional vs non-promotional days

---

## 3. Key Stakeholders and Roles

### Decision Makers
- **Maria Gonzalez, VP of Supply Chain** (Executive Sponsor)
  - Owns business case and ROI tracking
  - Final approval on deployment
  - Quarterly steering committee meetings

- **Roberto Diaz, Director of Store Operations** (Business Owner)
  - Defines operational requirements
  - Validates model outputs with field teams
  - Owns change management and training

### Data Science Team
- **Project Lead: Data Science Lead** (Modeling & Evaluation)
  - Algorithm selection, training, hyperparameter tuning
  - Model performance reporting

- **Data Engineer** (Data Preparation)
  - Data pipeline development
  - Feature engineering automation
  - Data quality monitoring

- **ML Engineer** (Deployment)
  - API development
  - Production monitoring
  - Model retraining pipeline

### Subject Matter Experts
- **Category Managers (33 product families)** (Domain Expertise)
  - Validate business logic of features
  - Provide context on promotions, seasonality, trends
  - Review forecasts for reasonableness

- **Store Managers (54 stores)** (End Users)
  - Provide feedback on forecast accuracy
  - Identify operational constraints
  - Primary users of forecast outputs

### Data Owners
- **IT Data Warehouse Team** (Data Access)
  - Provides historical sales, inventory, promotion data
  - Grants access to production databases
  - Ensures data privacy/security compliance

- **External Data Providers**
  - Oil price data (Ecuador's economy is oil-dependent)
  - Holiday calendar data
  - Weather data (future enhancement)

---

## 4. Project Scope

### In-Scope

**Data Sources:**
- Historical daily sales by store, product family, date (2013-2017)
- Store metadata (location, type, cluster, opening date)
- Product family metadata (perishability, category)
- Promotion calendar (dates, type, discount depth)
- Oil price data (daily WTI crude prices)
- Holiday calendar (national, regional, local events)

**Deliverables:**
1. Clean, feature-engineered dataset for modeling
2. Trained forecasting models with documented hyperparameters
3. Model evaluation report with business impact translation
4. Batch prediction pipeline (daily forecasts for next 16 days)
5. Model performance monitoring dashboard
6. Documentation for model maintenance team
7. Training materials for store managers

**Geographic Scope:**
- All 54 Favorita stores in Ecuador

**Product Scope:**
- All 33 product families (aggregated forecasts, not SKU-level)

**Time Scope:**
- Training data: 2013-01-01 to 2017-06-30
- Validation data: 2017-07-01 to 2017-12-31
- Test data: 2017-08-01 to 2017-08-15 (final holdout)

### Out-of-Scope

**Explicitly Not Included:**
- SKU-level forecasting (33 families, not 4,000+ SKUs)
- Real-time forecasting (daily batch updates are sufficient)
- Dynamic pricing optimization (separate future project)
- Cross-store inventory allocation (supply chain team owns this)
- International expansion (Ecuador only)
- New store forecasting (focus on existing stores with history)
- Weather data integration (deferred to Phase 2)

**Future Enhancements (Not in V1):**
- Promotion response modeling (what discount drives what lift)
- Cannibalization effects (one product's promotion hurting another)
- Clustering-based forecasts (segment stores by behavior)
- Explainability dashboard (what drives this week's forecast)

---

## 5. Constraints and Assumptions

### Technical Constraints

1. **Data Availability**
   - Historical data only goes back to 2013 (insufficient history for some seasonal patterns)
   - Data granularity is daily (cannot forecast intraday peaks)
   - Product family level only (no SKU-level data available)

2. **Computational Resources**
   - Training must complete within 8 hours on standard hardware (no GPU clusters)
   - Inference must generate forecasts for all stores/families within 30 minutes
   - Model size must fit in 2GB memory for deployment

3. **Latency Requirements**
   - Forecasts generated once daily (not real-time)
   - Acceptable lag: Forecasts for day T+1 must be ready by 6am on day T

### Business Constraints

1. **Budget**
   - Total project budget: $150K
   - No budget for commercial software licenses (open-source only)
   - No budget for external data purchases in V1

2. **Timeline**
   - Project must complete within 4 months (see Section 8)
   - Deployment must happen before Q4 2026 (holiday season)

3. **Organizational**
   - Store managers currently use Excel-based forecasts (change management required)
   - IT team has limited ML ops experience (simple deployment architecture needed)
   - Category managers must manually review forecasts before they go to stores (trust-building phase)

### Key Assumptions

1. **Data Quality**
   - Sales data is accurate and complete (no major gaps or data quality issues)
   - Store and product metadata is up-to-date
   - Promotion calendar accurately reflects in-store execution

2. **Business Process**
   - Store managers will act on forecasts (adoption is achieved through training)
   - Replenishment lead time remains stable at ~16 days
   - Current shrinkage and OOS measurement processes are reliable

3. **Modeling**
   - Historical patterns (2013-2017) are representative of future behavior
   - 4 years of data is sufficient to capture seasonality
   - Product family aggregation doesn't mask critical SKU-level dynamics

4. **External Factors**
   - No major economic disruptions (oil price shocks, policy changes)
   - Competitive landscape remains stable (no new stores opening nearby)
   - Product families remain consistent (no major category restructuring)

---

## 6. Risk Assessment

### High-Priority Risks

| Risk | Impact | Probability | Mitigation Strategy | Owner |
|------|--------|-------------|---------------------|-------|
| **Model doesn't beat baseline** | High | Medium | Start with simple baseline; iterate quickly; have fallback to rule-based system | Data Science Lead |
| **Data quality issues discovered late** | High | Medium | Conduct thorough data quality audit in Week 1-2; flag issues early | Data Engineer |
| **Store managers don't trust/use forecasts** | High | Medium | Involve managers early; show accuracy metrics; pilot with 5 stores first | Dir. of Operations |
| **Promotion data is incomplete** | Medium | High | Build model with and without promotion features; validate with category managers | Data Engineer |
| **IT cannot deploy model on time** | Medium | Medium | Use simple deployment (batch script, not complex API); start deployment early | ML Engineer |

### Medium-Priority Risks

| Risk | Impact | Probability | Mitigation Strategy | Owner |
|------|--------|-------------|---------------------|-------|
| **Computational constraints limit model complexity** | Medium | Low | Use efficient algorithms (XGBoost); sample data if needed; optimize code | Data Science Lead |
| **Seasonality patterns change post-2017** | Medium | Medium | Monitor model drift; plan for quarterly retraining | ML Engineer |
| **Key team members leave mid-project** | Medium | Low | Document all decisions; use version control; cross-train team | Project Lead |
| **External data (oil prices) unavailable** | Low | Low | Build model with and without oil features; use free data sources | Data Engineer |

---

## 7. Success Metrics Framework

### Technical Metrics (Model Performance)

**Primary Metric:** WMAPE (Weighted Mean Absolute Percentage Error) < 15%
**Why:** Gives more weight to high-volume products; interpretable for business stakeholders

**Secondary Metrics:**
- RMSE < 50 units/day (penalizes large errors)
- MAE < 30 units/day (interpretable)
- Forecast Bias within ±5% (no systematic over/under-forecasting)

**Segmented Reporting:**
All metrics will be reported by:
- Product family (33 segments)
- Store type (urban/suburban/rural)
- Day of week (weekday vs weekend)
- Promotional vs non-promotional periods

**Baseline Comparison:**
- Naive forecast: Sales[t] = Sales[t-7] (same day last week)
- Seasonal naive: Sales[t] = Sales[t-7] × (Avg last 4 weeks / Avg 4 weeks prior)
- Current Excel-based forecasts from store managers

### Business KPIs (Real-World Impact)

**Leading Indicators (Weeks 1-8 post-deployment):**
- Forecast adoption rate (% of stores using forecasts for ordering)
- Forecast review time (hours per week spent by category managers)
- Forecast override rate (% of forecasts manually adjusted)

**Lagging Indicators (Months 3-6 post-deployment):**
- Shrinkage rate reduction: Target 15% (from 2.8% to 2.38%)
- OOS rate reduction: Target 20% (from 6.5% to 5.2%)
- Stock turnover improvement: Target 2x/year increase for perishables
- Cost savings: Target $2.5M annual run-rate

**Measurement Approach:**
- A/B test: 5 pilot stores use forecasts, 5 control stores use current process
- Run pilot for 8 weeks before full rollout
- Track metrics weekly; report to steering committee monthly

### Translation Example: Technical → Business

| If Model Achieves | Then Business Sees | Because |
|-------------------|-------------------|---------|
| WMAPE = 15% | ~12% waste reduction | More accurate forecasts → less safety stock needed |
| RMSE = 45 units/day | ~18% OOS reduction | Fewer large errors → fewer stockouts on high-demand days |
| Bias = +3% | Slightly higher inventory | Slight over-forecasting is safer than under-forecasting |

---

## 8. Timeline and CRISP-DM Milestones

**Project Duration:** 16 weeks (4 months)
**Start Date:** March 1, 2026
**Target Deployment:** June 15, 2026

### Phase Breakdown

| Phase | Duration | Start | End | Key Deliverables | Success Criteria |
|-------|----------|-------|-----|------------------|------------------|
| **1. Business Understanding** | 1 week | Week 1 | Week 1 | Project charter, stakeholder map, success metrics | Signed charter; aligned business/ML goals |
| **2. Data Understanding** | 2 weeks | Week 2 | Week 3 | Data quality report, EDA notebook, data dictionary | All data sources accessible; quality issues documented |
| **3. Data Preparation** | 3 weeks | Week 4 | Week 6 | Feature engineering pipeline, train/val/test splits | Clean dataset; reproducible preprocessing code |
| **4. Modeling** | 4 weeks | Week 7 | Week 10 | Trained models, hyperparameter search results, baseline comparison | Model beats baseline; WMAPE < 15% on validation set |
| **5. Evaluation** | 2 weeks | Week 11 | Week 12 | Model evaluation report, business impact analysis, error analysis | Model approved by stakeholders; ROI confirmed |
| **6. Deployment** | 4 weeks | Week 13 | Week 16 | Batch prediction pipeline, monitoring dashboard, documentation | Forecasts delivered daily; pilot stores using outputs |

### Detailed Milestones

**Week 1: Business Understanding**
- Day 1-2: Stakeholder interviews (VP Supply Chain, Dir. Operations, Category Managers)
- Day 3-4: Define success criteria and document assumptions
- Day 5: Finalize and approve project charter
- **Deliverable:** This document

**Weeks 2-3: Data Understanding**
- Week 2: Data access setup; initial data profiling; data quality audit
- Week 3: Exploratory data analysis; visualize trends, seasonality, outliers
- **Deliverable:** EDA notebook + data quality report
- **Gate:** No critical data quality blockers identified

**Weeks 4-6: Data Preparation**
- Week 4: Clean data; handle missing values; merge datasets
- Week 5: Engineer time-based features (lags, rolling stats, seasonality)
- Week 6: Engineer external features (promotions, holidays, oil price); create train/val/test splits
- **Deliverable:** Feature engineering pipeline (Python scripts)
- **Gate:** Pipeline runs end-to-end; validation data is representative

**Weeks 7-10: Modeling**
- Week 7: Build baseline models (naive, seasonal naive)
- Week 8: Train candidate models (XGBoost, LightGBM, Prophet)
- Week 9: Hyperparameter tuning; cross-validation
- Week 10: Ensemble methods; final model selection
- **Deliverable:** Trained model artifacts + training notebook
- **Gate:** Model beats baseline by ≥10% on WMAPE; technical metrics met

**Weeks 11-12: Evaluation**
- Week 11: Error analysis (where/why does model fail); test set evaluation
- Week 12: Business impact translation; prepare stakeholder presentation; get approval
- **Deliverable:** Evaluation report + stakeholder presentation
- **Gate:** Stakeholders approve model for pilot deployment

**Weeks 13-16: Deployment**
- Week 13: Build batch prediction pipeline; set up monitoring
- Week 14: Create documentation; train store managers
- Week 15: Pilot launch (5 stores); monitor daily
- Week 16: Gather feedback; iterate; prepare for full rollout
- **Deliverable:** Production pipeline + pilot results
- **Gate:** Pilot stores successfully using forecasts; no critical issues

### Post-Project (Weeks 17+)

- **Week 17-24:** Full rollout to all 54 stores
- **Month 3-6:** Monitor business KPIs (shrinkage, OOS)
- **Month 6:** ROI assessment; lessons learned; plan Phase 2 enhancements

---

## 9. Dependencies and Handoffs

### External Dependencies

1. **IT Data Warehouse Team** (Week 1-2)
   - Grant database access to data science team
   - Provide data dictionary and schema documentation

2. **Category Managers** (Week 3, Week 12)
   - Validate promotion calendar accuracy (Week 3)
   - Review model outputs for business reasonableness (Week 12)

3. **IT Operations** (Week 13-15)
   - Provision server for batch prediction pipeline
   - Set up monitoring and alerting infrastructure

### Handoff Plan

| From | To | What | When |
|------|-----|------|------|
| Data Engineer | Data Science Lead | Clean dataset + feature pipeline | End of Week 6 |
| Data Science Lead | ML Engineer | Trained model artifacts | End of Week 10 |
| ML Engineer | Dir. of Operations | Deployed prediction pipeline | End of Week 16 |
| Dir. of Operations | Store Managers | Forecast outputs + training | Week 17+ |
| ML Engineer | IT Operations | Ongoing monitoring & retraining plan | End of Week 16 |

---

## 10. Approval and Sign-Off

### Approvers

This project charter must be approved by:

- [ ] **Maria Gonzalez, VP of Supply Chain** (Executive Sponsor)
  _Approves business case, ROI targets, and budget_

- [ ] **Roberto Diaz, Director of Store Operations** (Business Owner)
  _Approves operational requirements and success criteria_

- [ ] **Data Science Lead** (Technical Lead)
  _Confirms feasibility of technical approach and timeline_

- [ ] **IT Director** (Infrastructure Owner)
  _Confirms IT can support deployment requirements_

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | March 1, 2026 | Data Science Lead | Initial charter created |

---

## Appendices

### A. Glossary of Terms

- **CRISP-DM:** Cross-Industry Standard Process for Data Mining
- **MAPE:** Mean Absolute Percentage Error = (1/n) × Σ |Actual - Forecast| / Actual × 100%
- **WMAPE:** Weighted MAPE = Σ |Actual - Forecast| / Σ Actual × 100%
- **RMSE:** Root Mean Squared Error = √[(1/n) × Σ (Actual - Forecast)²]
- **MAE:** Mean Absolute Error = (1/n) × Σ |Actual - Forecast|
- **OOS:** Out-of-Stock (product unavailable when customer wants to buy)
- **Shrinkage:** Inventory loss due to waste, theft, or damage
- **Product Family:** Aggregated product category (e.g., "Dairy" includes milk, yogurt, cheese)
- **Lead Time:** Time between placing an order and receiving inventory (16 days for Favorita)

### B. Reference Documents

- Kaggle Dataset: "Store Sales — Time Series Forecasting"
- CRISP-DM Methodology Guide (internal)
- Retail Forecasting Best Practices (internal)
- Favorita Supply Chain Playbook (internal)

### C. Contact Information

- **Project Lead:** Data Science Lead — ds-lead@favorita.ec
- **Executive Sponsor:** Maria Gonzalez — maria.gonzalez@favorita.ec
- **Business Owner:** Roberto Diaz — roberto.diaz@favorita.ec
- **Project Slack Channel:** #favorita-forecast-2026

---

**Document Status:** DRAFT — Pending Approval
**Next Review Date:** March 8, 2026
