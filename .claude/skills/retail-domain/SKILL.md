---
name: retail-domain
description: "Retail and grocery domain knowledge for data science. Activates when working with store sales, product categories, promotions, inventory, supply chain, or grocery retail concepts."
---

# Retail & Grocery Domain Knowledge

## Instructions

Apply retail-specific domain knowledge when the user works on grocery/retail data science problems.

### Key Retail KPIs

When discussing business goals or evaluation metrics, reference these standard retail KPIs:

- **Sales per sqm** — Revenue per square meter of selling space
- **Basket size** — Average number of items per transaction
- **Average transaction value (ATV)** — Revenue per transaction
- **Shrinkage rate** — Loss from waste, theft, damage (typically 1-3% in grocery)
- **Out-of-stock rate (OOS)** — Percentage of SKUs unavailable when demanded
- **Stock turnover** — How often inventory is sold and replaced per period
- **Gross margin return on investment (GMROI)** — Gross profit / average inventory cost
- **Promotion uplift** — Incremental sales attributed to a promotion
- **Price elasticity** — Demand sensitivity to price changes per product category
- **Customer footfall** — Number of store visitors per period

### Grocery-Specific Data Patterns

Alert the user to these common patterns in grocery retail data:

- **Seasonality**: Weekly (weekend peaks), monthly (payday effects), annual (holidays, summer)
- **Promotion effects**: Cannibalization across related products, stockpiling behavior, post-promo dip
- **Perishability**: Fresh categories (bakery, produce, dairy) have different forecasting needs than shelf-stable
- **External factors**: Weather impacts fresh produce and beverages; fuel prices affect store traffic
- **Holiday effects**: Easter, Christmas, national holidays create spikes; day-before effects are often larger than the day itself
- **Store clustering**: Urban vs suburban vs rural stores behave differently; store size matters

### Product Family Taxonomy (Common in Grocery)

When working with product categories, use this typical hierarchy:
- Department → Category → Subcategory → Brand → SKU
- Example: Fresh → Dairy → Yogurt → Danone → Danone Natural 500g

Common product families in the tutorial dataset:
AUTOMOTIVE, BABY CARE, BEAUTY, BEVERAGES, BOOKS, BREAD/BAKERY, CELEBRATION, CLEANING, DAIRY, DELI, EGGS, FROZEN FOODS, GROCERY I, GROCERY II, HARDWARE, HOME AND KITCHEN, HOME APPLIANCES, HOME CARE, LADIESWEAR, LAWN AND GARDEN, LINGERIE, LIQUOR/WINE/BEER, MAGAZINES, MEATS, PERSONAL CARE, PET SUPPLIES, PLAYERS AND ELECTRONICS, POULTRY, PREPARED FOODS, PRODUCE, SCHOOL AND OFFICE SUPPLIES, SEAFOOD

### Forecasting Considerations for Retail

Guide the user toward these best practices:
- Always use a time-based train/test split (never random split for time series)
- Include lag features (sales 7, 14, 28 days ago)
- Include rolling statistics (7-day, 28-day rolling mean/std)
- Day-of-week and month-of-year as cyclical features
- Promotion flags and promotion type as features
- Oil price as a macroeconomic indicator (especially for Ecuadorian data)
- Holiday flags (with lead/lag for pre-holiday shopping)
- Evaluate per store and per product family, not just overall

### Personalization Note

This skill contains generic retail knowledge. To adapt for YOUR organization:
- Replace the KPI definitions with your company's specific metric definitions
- Add your product hierarchy and category naming conventions
- Include your company's seasonal calendar and promotion types
- Add store-specific attributes relevant to your chain (format, location tier, etc.)
