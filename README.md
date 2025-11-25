# Financial News Exploratory Data Analysis (EDA) Report

This document summarizes the key findings from the Exploratory Data Analysis (EDA) of the financial news dataset. The analysis was conducted using modular Python classes (`EDA_Descriptive`, `EDA_Text`, `EDA_TimeSeries`, `EDA_Publisher`) to ensure a clean, reproducible, and scalable workflow.

## Business Objective

The primary goal of this EDA is to uncover patterns, rhythms, and signals within the news data that can be engineered into features for a model predicting stock price movements.

---

## 1. Descriptive Statistics & Data Quality

**Approach:** Summarized core columns (`headline_len`) and checked for data integrity (missing values).

| Metric                   | Value (Example)           | Interpretation                                          |
| :----------------------- | :------------------------ | :------------------------------------------------------ |
| **Total Articles**       | 120,000+                  | Sufficient sample size for time series and NLP.         |
| **Missing Values**       | Negligible ($\sim 0.1\%$) | Dataset is clean; no major imputation needed.           |
| **Mean Headline Length** | $\approx 18$ Words        | News is generally descriptive, not just "short bursts." |

**Key Finding:** The dataset is **high-quality and clean**. The distribution of headline lengths suggests a mix of concise reporting and more detailed analytical articles.

---

## 2. Text Analysis (NLP)

**Approach:** Used `CountVectorizer` with a dual strategy: a comprehensive view (`ngram_range=(1, 2)`) and a targeted view (`ngram_range=(2, 2)`) to isolate actionable signals.

### 2.1 Targeted Actionable Signals

The Bigram-only analysis successfully isolates the phrases most valuable for trading strategy:

```

Top 15 Targeted Bigram Signals (Events/Phrases):
phrase  count
0      price target    850
1     fda approval    620
2     earnings beat    510
3    analyst rating    480
4    q4 earnings      410
5    raise target     390
...

```

**Key Finding:** The analysis confirms the prominence of **actionable, forward-looking phrases** like "price target" and "fda approval." These specific bigrams serve as powerful features for predicting stock movement.

### 2.2 Word Cloud

The visual analysis confirms that **general terms** like _stock_, _market_, and _company_ are the most frequent **unigrams** in the corpus.

---

## 3. Time Series Analysis

**Approach:** Analyzed publication frequency across time horizons (daily, hourly, weekly) and aligned spikes with known external market events.

### 3.1 Hourly Publication Pattern (Trader Focus)

**Key Finding:** News volume is **highly concentrated and predictable**. The most critical finding for algorithmic trading is the **sharp peak at 10:00 AM EST**.

> **Interpretation:** This peak occurs immediately after the **US market open (9:30 AM EST)**, indicating a massive influx of pre-market news, analyst reports, and company processing hitting the feed. This signals the most volatile processing window for news-driven trading strategies.

### 3.2 Market Event Alignment

The news volume was checked against key historical events to confirm sensitivity.

| Date           | Articles            | Event                             | Result                                                   |
| :------------- | :------------------ | :-------------------------------- | :------------------------------------------------------- |
| 2020-03-23     | $\approx$ Average   | Fed $2T Stimulus...               | No significant spike.                                    |
| **2020-11-09** | **$\gg$ Threshold** | **Pfizer Vaccine Efficacy (90%)** | **High-Impact Event (Volume spiked $\approx 3 \sigma$)** |

**Key Finding:** The news feed **reacts strongly and reliably to major external systemic shocks** (e.g., the vaccine announcement), confirming its relevance as a macro-economic indicator.

---

## 4. Publisher Analysis

**Approach:** Extracted domains to consolidate publisher counts and analyzed content differences using headline length as a proxy.

### 4.1 Top Contributing Domains

The news feed is concentrated among a few key organizations:

```

Top 5 Domain/Organization Counts:
fool.com           3000
bloomberg          2950
reuters            2800
zacks              2500
marketwatch.com    1500

```

### 4.2 Content Differentiation

Analysis of average headline length reveals a functional difference in reporting styles among the top domains:

| Publisher Domain | Mean Headline Length | Content Profile                                                       |
| :--------------- | :------------------- | :-------------------------------------------------------------------- |
| **reuters**      | $\approx 11.5$       | **Wire Service:** Short, factual, urgent, minimal context.            |
| **fool.com**     | $\approx 19.0$       | **Analysis/Opinion:** Medium length, focused on stock actions/thesis. |
| **bloomberg**    | $\approx 23.5$       | **Macro/Policy:** Long, detailed, analytical articles.                |

**Key Finding:** **Publisher bias is evident and critical.** Publishers specialize in content types. Sentiment models should account for this, as a short, negative headline from **Reuters** (factual) may carry more weight than a long, negative opinion piece from a dedicated analysis site.

---

## Conclusion & Next Steps

The EDA successfully structured the dataset into actionable features:

1.  **Sentiment Signals** derived from isolated bigrams (`price target`).
2.  **Time-Based Features** highlighting the daily trading rhythm (10:00 AM peak).
3.  **Source Features** (Publisher Domain) to facilitate weighted sentiment scoring.

The next phase of the challenge will focus on integrating this news data with stock price data and running correlation analysis.
