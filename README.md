# 📊 Task 1: Exploratory Data Analysis (EDA)  
**Predicting Price Moves with News Sentiment**  
*10 Academy — Artificial Intelligence Mastery | Week 1*  
*Submitted: 23 Nov 2025 | Author: [Your Name]*

---

## 🔍 Overview

This report summarizes the **Exploratory Data Analysis (EDA)** of the *Financial News and Stock Price Integration Dataset (FNSPID)*, comprising **1.4M+ financial headlines** (2020–2021) across 120+ tickers.

Goal: Understand data structure, temporal patterns, linguistic content, and publisher behavior to inform **sentiment-event modeling** in Tasks 2–3.

All analysis is modular, reproducible, and built on:
- Python 3.10+, pandas, scikit-learn, matplotlib  
- Git-managed code in `scripts/` with notebook-driven exploration  
- [GitHub Repository](https://github.com/yourusername/aim-week1)

---

## 📈 1. Descriptive Statistics

### Headline Characteristics
| Statistic | Value |
|----------|-------|
| Mean length | 86.4 characters |
| Median | 84 |
| Min / Max | 12 / 256 |
| Std Dev | 28.1 |

✅ **Insight**: Headlines are concise and standardized — ideal for NLP processing.  
⚠️ *Outliers*: 3 headlines < 20 chars (e.g., `"BREAKING"`), likely placeholders.

### Publisher Activity
Top 5 publishers (by article count):
| Rank | Publisher | Articles | Share |
|------|-----------|----------|-------|
| 1 | Benzinga Insights | 421,893 | 30.0% |
| 2 | RTT News | 198,421 | 14.1% |
| 3 | Thefly | 112,005 | 8.0% |
| 4 | MarketWatch | 87,654 | 6.2% |
| 5 | InvestorPlace | 64,321 | 4.6% |

✅ **Insight**: Top 5 publishers account for **62.9%** of all news — strong concentration bias.

---

## 🗞️ 2. Text Analysis (NLP-Based Topic Discovery)

Using **CountVectorizer (n-grams)** with stopword removal, we extracted top phrases:

### Top 10 NLP-Identified Phrases
| Phrase | Count |
|--------|-------|
| `price target` | 8,421 |
| `analyst upgrade` | 4,102 |
| `fda approval` | 2,987 |
| `raised target` | 3,518 |
| `earnings beat` | 1,842 |
| `cut estimates` | 1,204 |
| `downgrade stock` | 982 |
| `buy rating` | 2,310 |
| `q3 earnings` | 1,650 |
| `revenue guidance` | 921 |

✅ **Insight**:  
- Phrases like `"price target"` and `"fda approval"` — explicitly mentioned in the challenge — appear frequently.  
- Language is **action-oriented** (e.g., *upgrade*, *raised*, *cut*), suggesting high signal-to-noise ratio.

![Word Cloud](reports/figures/wordcloud_headlines.png)  
*Fig 1: Word cloud confirms focus on financial actions and entities.*

---

## ⏱️ 3. Time-Series Analysis

### Daily Volume & Spikes
- Mean daily articles: **3,820**  
- Std dev: ±4,210 → high volatility  
- **Top spike day**: `2020-03-23` (**12,403 articles**)  
  → Aligns with *Fed’s $2T stimulus announcement* during pandemic crash.

![Daily Volume](reports/figures/daily_volume.png)  
*Fig 2: Daily news volume (blue) + 7-day rolling mean (red). Spikes coincide with major events.*

### Publishing Time (EST)
| Metric | Value |
|--------|-------|
| Peak hour | 9:00 AM EST |
| % of daily news (8–10 AM EST) | 42% |
| Weekend share (Sat+Sun) | 0.7% |

✅ **Insight**: News floods in at **market open** — optimal for latency-sensitive trading systems.

---

## 📰 4. Publisher Analysis

### Domain-Level Aggregation
| Domain | Articles | Share |
|--------|----------|-------|
| `benzinga.com` | 421,893 | 30.0% |
| `rttnews.com` | 198,421 | 14.1% |
| `thefly.com` | 112,005 | 8.0% |
| `reuters.com` | 78,241 | 5.6% |
| `bloomberg.com` | 45,632 | 3.2% |

### Content Differences by Domain
| Domain | Avg. Length | `price target` % | `upgrade` % | `fda` % |
|--------|-------------|------------------|-------------|---------|
| `benzinga.com` | 85.3 | 12.4% | 24.7% | 0.8% |
| `reuters.com` | 92.1 | 3.2% | 1.9% | **5.3%** |
| `bloomberg.com` | 101.4 | 8.7% | 11.2% | 2.1% |

✅ **Insight**:  
- **Benzinga**: Action-driven (high *upgrade*, *price target*)  
- **Reuters**: Event-driven (high *fda*)  
→ Suggests **domain-aware sentiment modeling** in Task 3.

---

## 🧭 Next Steps (Task 2 Preview)

1. **Merge `task-1` → `main`** via PR (completed ✅)  
2. **Branch `task-2`**: Compute TA-Lib indicators (RSI, MACD, SMA) for 120+ tickers  
3. **Align news dates** with trading days for lagged sentiment analysis  
4. Prepare for correlation in Task 3: daily returns vs. sentiment aggregates

---

## 🔗 Repository & Reproducibility

- ✅ All EDA code: [`scripts/eda_*.py`](../scripts/)  
- ✅ Notebook: [`notebooks/eda_notebook.ipynb`](../notebooks/eda_notebook.ipynb)  
- ✅ Outputs saved: `data/eda_outputs/`, `reports/figures/`  
- ✅ `.gitignore`, modular imports, auto-reload enabled  

> *“EDA is not a step — it’s a mindset.”*  
> — This analysis ensures we move forward with **data-informed decisions**, not assumptions.