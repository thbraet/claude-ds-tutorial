# Project Charter: Favorita Store Sales Forecasting

**Project ID:** FAVORITA-FORECAST-2026
**Version:** 1.0
**Date:** March 1, 2026
**Status:** Draft — Pending Approval

---

## 1. Executive Summary

Favorita, Ecuador's leading grocery retailer, seeks to improve inventory management across 54 stores and 33 product families through machine learning-based sales forecasting. The project will leverage 4+ years of historical sales data (2013-2017) to predict daily demand 16 days ahead, enabling optimized replenishment decisions.

**Expected outcomes:**
- 15% reduction in overstock waste ($1.8M annual savings)
- 20% reduction in out-of-stock incidents ($700K protected revenue)
- Improved customer satisfaction through better product availability

The project follows the CRISP-DM methodology with a 16-week timeline from kickoff to pilot deployment.

---

## 2. Business Context and Problem Statement

### Current Situation

Favorita operates 54 grocery stores across Ecuador, managing inventory for 33 product families ranging from shelf-stable goods to highly perishable items. Current forecasting relies on:
- Store manager intuition and experience
- Basic Excel-based trend analysis
- Manual adjustments for promotions and holidays

### The Problem

This approach results in:
- **Overstock waste**: 2.8% shrinkage rate, particularly in perishables (Produce, Dairy, Bakery, Meats)
- **Stockouts**: 6.5% out-of-stock rate, causing lost sales and customer frustration
- **Inefficient labor**: Store managers spend 5+ hours weekly on manual forecasting

### Why Now?

- Historical data is now available in a consolidated data warehouse
- Competitive pressure from new market entrants
- Leadership mandate to reduce waste as part of sustainability initiative
- Successful pilot projects in other retail analytics areas

### Business Value

| Impact Area | Annual Value |
|-------------|--------------|
| Waste reduction (15% of shrinkage) | $1.8M |
| Protected revenue (20% fewer stockouts) | $700K |
| Labor efficiency (automated forecasts) | $150K |
| **Total** | **$2.65M** |

---

## 3. Objectives and Success Criteria

### Primary Objectives

| Objective | Current State | Target | Measurement |
|-----------|---------------|--------|-------------|
| Reduce overstock waste | 2.8% shrinkage | 2.38% shrinkage | Monthly shrinkage reports |
| Reduce stockouts | 6.5% OOS rate | 5.2% OOS rate | Weekly OOS tracking |
| Automate forecasting | Manual process | Daily automated forecasts | System uptime metrics |

### Technical Success Criteria

| Metric | Target | Rationale |
|--------|--------|-----------|
| WMAPE (Weighted Mean Absolute % Error) | < 15% | Primary metric; weights high-volume items appropriately |
| RMSE (Root Mean Squared Error) | < 50 units/day | Penalizes large forecast errors |
| MAE (Mean Absolute Error) | < 30 units/day | Interpretable in business terms |
| Forecast Bias | ± 5% | Ensures no systematic over/under-forecasting |
| Beat baseline | > 10% improvement | Must outperform naive same-day-last-week |

### Evaluation Strategy

- Time-based train/validation/test split (no data leakage)
- Rolling window backtesting on final 6 months
- Segmented analysis by: product family, store type, promotional periods

---

## 4. Scope

### In Scope

**Data:**
- Daily sales transactions (2013-01-01 to 2017-08-15)
- Store metadata (54 stores: location, type, cluster)
- Product family metadata (33 families: category, perishability)
- Promotion calendar (dates, participating stores/families)
- Oil price data (Ecuador's economy is oil-dependent)
- Holiday calendar (national, regional, local, transferred holidays)

**Deliverables:**
- Clean, feature-engineered dataset
- Trained forecasting model(s) with documented parameters
- Batch prediction pipeline (daily 16-day forecasts)
- Model evaluation report with business impact analysis
- Monitoring dashboard for forecast accuracy
- Documentation and training materials

**Geographic:** All 54 Favorita stores in Ecuador

**Product:** All 33 product families (aggregated, not SKU-level)

### Out of Scope

| Item | Reason |
|------|--------|
| SKU-level forecasting | Data not available; family-level sufficient for replenishment |
| Real-time forecasting | Daily batch meets business needs |
| Dynamic pricing optimization | Separate initiative with different stakeholders |
| New store forecasting | Focus on stores with historical data |
| Weather data integration | Deferred to Phase 2 |
| Cross-store inventory transfers | Supply chain team owns this process |

### Future Enhancements (Phase 2)

- Promotion response modeling
- Weather impact integration
- Store clustering for improved accuracy
- Forecast explainability dashboard

---

## 5. Data Sources

### Primary Data

| Dataset | Description | Granularity | Records |
|---------|-------------|-------------|---------|
| `train.csv` | Historical sales | Store × Family × Date | ~3M rows |
| `stores.csv` | Store metadata | Store | 54 rows |
| `transactions.csv` | Daily transaction counts | Store × Date | ~83K rows |
| `oil.csv` | Daily oil prices (WTI) | Date | ~1.2K rows |
| `holidays_events.csv` | Holiday calendar | Date × Region | ~350 rows |

### Data Characteristics

- **Date range**: January 1, 2013 — August 15, 2017
- **Target variable**: `sales` (daily unit sales, can include returns as negative values)
- **Key challenge**: `onpromotion` column has missing values before 2014

### Data Quality Considerations

- Store 52 opened mid-2015 (limited history)
- Some product families have zero sales periods (new products, seasonal)
- "Transfers" column represents inter-store movements, not customer sales
- Regional holidays require careful encoding (not all stores affected)

---

## 6. Timeline and CRISP-DM Phases

**Project Duration:** 16 weeks
**Start Date:** March 1, 2026
**Target Deployment:** June 15, 2026

### Phase Schedule

```
Week  1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16
      |-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
      [BU ]
           [  Data Understanding  ]
                      [    Data Preparation     ]
                                        [       Modeling        ]
                                                            [ Eval  ]
                                                                   [     Deployment      ]
```

### Detailed Milestones

| Phase | Weeks | Deliverables | Gate Criteria |
|-------|-------|--------------|---------------|
| **Business Understanding** | 1 | Project charter, stakeholder alignment | Charter approved |
| **Data Understanding** | 2-3 | EDA notebook, data quality report, data dictionary | No critical data blockers |
| **Data Preparation** | 4-6 | Feature pipeline, train/val/test splits | Pipeline reproducible end-to-end |
| **Modeling** | 7-10 | Trained models, hyperparameter results, baseline comparison | Model beats baseline by ≥10% |
| **Evaluation** | 11-12 | Error analysis, business impact report | Stakeholder approval for pilot |
| **Deployment** | 13-16 | Batch pipeline, monitoring, pilot with 5 stores | Forecasts delivered daily |

### Key Checkpoints

- **Week 3**: Data quality sign-off — proceed or pause for remediation
- **Week 10**: Model selection — choose final algorithm
- **Week 12**: Go/no-go for pilot deployment
- **Week 16**: Pilot results review — plan full rollout

---

## 7. Risks and Mitigation Strategies

### High-Priority Risks

| Risk | Impact | Likelihood | Mitigation | Owner |
|------|--------|------------|------------|-------|
| Model doesn't beat baseline | High | Medium | Start with simple baseline; iterate quickly; have fallback to rule-based system | DS Lead |
| Data quality issues discovered late | High | Medium | Conduct thorough data audit in Weeks 1-2; document all issues early | Data Engineer |
| Store managers don't adopt forecasts | High | Medium | Involve managers in requirements; pilot with champions; show accuracy metrics | Dir. Operations |
| Promotion data incomplete | Medium | High | Build model with/without promotion features; validate with category managers | Data Engineer |

### Medium-Priority Risks

| Risk | Impact | Likelihood | Mitigation | Owner |
|------|--------|------------|------------|-------|
| Computational constraints | Medium | Low | Use efficient algorithms (XGBoost); optimize code; sample if needed | ML Engineer |
| Key team member leaves | Medium | Low | Document all decisions; cross-train team; use version control | Project Lead |
| IT deployment delays | Medium | Medium | Start deployment planning early; use simple architecture | ML Engineer |
| Historical patterns don't generalize | Medium | Medium | Monitor drift post-deployment; plan quarterly retraining | DS Lead |

### Risk Response Plan

1. **Weekly risk review** in team standup
2. **Escalation path**: DS Lead → Dir. Operations → VP Supply Chain
3. **Contingency budget**: 2 weeks buffer built into timeline

---

## 8. Team Roles and Responsibilities

### Core Team

| Role | Name | Responsibilities |
|------|------|------------------|
| **Executive Sponsor** | Maria Gonzalez (VP Supply Chain) | Budget approval, strategic decisions, executive reporting |
| **Business Owner** | Roberto Diaz (Dir. Store Operations) | Requirements validation, change management, pilot oversight |
| **Data Science Lead** | TBD | Model development, technical decisions, evaluation |
| **Data Engineer** | TBD | Data pipelines, feature engineering, data quality |
| **ML Engineer** | TBD | Deployment, monitoring, production support |

### Extended Team

| Role | Involvement | Responsibilities |
|------|-------------|------------------|
| **Category Managers** | Weekly consults | Domain expertise, validate business logic, review forecasts |
| **Store Managers (Pilot)** | Pilot phase | End-user feedback, adoption testing |
| **IT Data Warehouse** | As needed | Data access, schema documentation |
| **IT Operations** | Weeks 13-16 | Server provisioning, monitoring infrastructure |

### RACI Matrix

| Activity | Sponsor | Bus. Owner | DS Lead | Data Eng | ML Eng |
|----------|---------|------------|---------|----------|--------|
| Approve charter | A | R | C | I | I |
| Data quality audit | I | I | A | R | C |
| Feature engineering | I | C | A | R | C |
| Model training | I | I | R | C | C |
| Evaluation report | A | R | R | C | C |
| Deployment | I | A | C | C | R |
| Pilot oversight | I | R | C | I | C |

*R = Responsible, A = Accountable, C = Consulted, I = Informed*

---

## 9. Approval

### Sign-Off Required

- [ ] **Maria Gonzalez**, VP Supply Chain — Business case and budget
- [ ] **Roberto Diaz**, Dir. Store Operations — Requirements and success criteria
- [ ] **Data Science Lead** — Technical feasibility and timeline
- [ ] **IT Director** — Infrastructure and deployment support

### Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | March 1, 2026 | Data Science Lead | Initial charter |

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| CRISP-DM | Cross-Industry Standard Process for Data Mining |
| WMAPE | Weighted Mean Absolute Percentage Error |
| OOS | Out-of-Stock |
| Shrinkage | Inventory loss due to waste, theft, or damage |
| Product Family | Aggregated product category (e.g., "Dairy" includes milk, yogurt, cheese) |
| Lead Time | Time between placing an order and receiving inventory (~16 days) |

## Appendix B: References

- Kaggle Dataset: [Store Sales — Time Series Forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting)
- Project Charter: `docs/project-charter.md` (this document)
- CLAUDE.md: Project conventions and context
