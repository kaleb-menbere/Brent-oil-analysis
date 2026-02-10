# **Task 1: Data Exploration, Workflow, and Model Understanding**

**Project:** Brent Oil Price Analysis
**Client Context:** Birhan Energies – Energy Market Intelligence

---

## 1. Objective of the Analysis

The objective of this task is to explore historical Brent crude oil price data, understand its structure and limitations, and design a robust analysis workflow that supports time series modeling and change point detection. The ultimate goal is to assess how major geopolitical, economic, and policy-related events influence oil price dynamics over time.

---

## 2. Dataset Overview

### 2.1 Brent Oil Price Dataset

* **File:** `BrentOilPrices.csv`
* **Total records:** 9,011
* **Columns:**

  * `Date`
  * `Price`
* **Date range:** 20 May 1987 – 14 November 2022
* **Time span:** ~35.5 years

The dataset contains historical Brent crude oil prices observed over multiple decades, covering several major global economic cycles and geopolitical events.

---

## 3. Data Structure and Initial Findings

### 3.1 Data Types and Schema

* The `Date` column is initially stored as an **object** type and requires conversion to a datetime format.
* The conversion to datetime was successful for **100% of records**, indicating no invalid date values.
* A warning was raised during parsing due to **unspecified date format**, meaning Pandas relied on flexible inference.

> While all dates were successfully parsed, relying on automatic inference may introduce inconsistencies and should be avoided in production workflows.

---

### 3.2 Temporal Coverage and Continuity

* The dataset spans **35.5 years**, making it suitable for long-term trend and regime-shift analysis.
* However, **3,952 dates are missing from the continuous daily range**.

This indicates that:

* The data is **not strictly daily**
* Missing dates likely correspond to:

  * Weekends
  * Market holidays
  * Periods of non-reporting

### Records per year show:

* Early years (e.g., 1987) have fewer observations
* Later years are more consistent but still not perfectly uniform

This irregular spacing is a critical consideration for time series modeling.

---

## 4. Key Data Issues, Limitations, and Problems Identified

### 4.1 Irregular Time Series (Missing Dates)

**Problem:**
Nearly 4,000 dates are missing from the expected continuous range.

**Impact:**

* Some time series models assume regular intervals
* Rolling statistics, differencing, and volatility estimation may be biased if gaps are ignored

**Mitigation:**

* Explicitly set the `Date` column as the index
* Decide whether to:

  * Reindex to daily frequency and leave gaps as NaN
  * Forward-fill prices (with caution)
  * Work with returns rather than raw prices

---

### 4.2 Non-Stationary Price Series

**Problem:**
Brent oil prices exhibit long-term trends and structural shifts.

**Impact:**

* Many statistical models assume stationarity
* Direct modeling of raw prices can lead to misleading inference

**Mitigation:**

* Use log prices or log returns
* Apply differencing
* Perform stationarity tests (ADF test) before modeling

---

### 4.3 Date Parsing Warning

**Problem:**
Pandas raised a warning indicating it could not infer a consistent date format.

**Impact:**

* Inconsistent parsing could lead to subtle ordering or alignment issues
* Reproducibility is reduced

**Mitigation:**

* Explicitly specify the date format during parsing
* Enforce strict datetime conversion in preprocessing

---

### 4.4 Lack of Explanatory Variables

**Problem:**
The dataset contains **only price data**, with no accompanying explanatory variables.

**Impact:**

* Change point detection can identify *when* prices changed
* It cannot explain *why* prices changed without external context

**Mitigation:**

* Enrich the dataset with:

  * Geopolitical event timelines
  * OPEC policy decisions
  * Economic shocks (e.g., COVID-19, financial crises)

---

### 4.5 Event Attribution and Causality

**Problem:**
Even when change points align with known events, the relationship is correlational.

**Impact:**

* There is a risk of over-interpreting statistical breaks as causal effects

**Mitigation:**

* Clearly communicate that results indicate **temporal association**, not causation
* Support findings with domain knowledge and external references

---

## 5. Planned Data Enrichment

To improve interpretability and analytical value, the following enrichment is planned:

* Curated dataset of major oil-related events:

  * OPEC production decisions
  * Wars and geopolitical conflicts
  * Sanctions and trade restrictions
  * Global economic crises
* Alignment of event dates with detected change points
* Categorization of events by type (geopolitical, economic, policy)

This enrichment enables contextual interpretation of detected structural breaks.

---

## 6. Preprocessing Plan for Time Series Analysis

Based on the exploration results, the following preprocessing steps are planned:

1. Convert `Date` to datetime with explicit format
2. Sort data chronologically
3. Set `Date` as the index
4. Handle missing dates explicitly (reindexing strategy)
5. Compute:

   * Log prices
   * Log returns
6. Test for stationarity (ADF test)
7. Visualize trends, volatility, and rolling statistics

---

## 7. Time Series Properties and Model Understanding

### 7.1 Trend and Regime Behavior

Brent oil prices display long-term upward and downward trends influenced by global supply-demand dynamics. Periods of stability are often interrupted by sharp structural changes.

---

### 7.2 Volatility Characteristics

* High volatility clustering during crisis periods
* Relatively calm periods during stable supply-demand conditions
* Justifies the use of regime-switching or change point models

---

### 7.3 Change Point Modeling Rationale

Change point models are well-suited for this dataset because they:

* Identify structural breaks without pre-specifying event dates
* Quantify uncertainty around regime shifts
* Allow comparison of price behavior before and after breaks

---

## 8. Expected Outputs

* Identified change point dates
* Estimated mean and variance before and after each change
* Posterior uncertainty estimates (Bayesian approach)
* Contextual interpretation using enriched event data

---

## 9. Summary

This exploratory analysis confirms that the Brent oil price dataset is rich, long-term, and suitable for structural change analysis. However, it also presents challenges such as irregular time spacing, non-stationarity, and lack of explanatory variables. Addressing these limitations through careful preprocessing and data enrichment is essential for reliable modeling and interpretation.
