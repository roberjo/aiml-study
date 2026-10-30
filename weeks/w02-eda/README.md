# W2 · Nov 9 — pandas, cleaning, EDA, plotting: Wikipedia attention demand

What is the internet paying attention to, who is actually doing the reading (humans or bots),
and when? Replaces the course's ride-sharing case with the same skills on livelier data.

Running log of setup, decisions and problems: [LOG.md](LOG.md).

## Learn
- [ ] [Python for Data Analysis, 3rd ed.](https://wesmckinney.com/book/), chapters 5–9 (skim what you know)
- [ ] [Kaggle Learn: Pandas](https://www.kaggle.com/learn/pandas)
- [ ] [Kaggle Learn: Data Visualization](https://www.kaggle.com/learn/data-visualization)
- [ ] Google ML Crash Course: [Numerical data](https://developers.google.com/machine-learning/crash-course/numerical-data)
- [ ] Optional: [Polars user guide](https://docs.pola.rs/user-guide/getting-started/), "Getting started" and "Expressions"

## Build
- [ ] **Data:** `uv run python weeks/w02-eda/get_data.py --dump` (about 4 minutes, ~70 MB into `data/w02/`)
- [ ] **Raw pass:** `uv run marimo edit weeks/w02-eda/raw.py`. Implement the seven stubs
      (parse_line, describe, group_sum, weekday_means, fill_missing_days, rolling_median,
      find_spikes) in plain Python until every check is ✅
- [ ] **Framework pass:** `uv run marimo edit weeks/w02-eda/build.py`. Read the worked examples,
      fill in the four YOUR TURN cells (A–D) with Polars and DuckDB, and run the race in section 6
- [ ] Answer the questions from both notebooks below
- [ ] Three spikes explained with the real-world event behind each

Suggested pacing: book chapters + Kaggle Pandas on weeknight 1; `raw.py` on weeknight 2;
Saturday for `build.py`, the questions, and the crash course module.

## Data

| File | What | Rows |
|---|---|---|
| `articles_daily.parquet` | 27 English Wikipedia articles, daily, by agent (user / automated / spider), Jan 2024 to Sep 2026 | ~80k |
| `site_daily.parquet` | All of English Wikipedia, daily, by agent | ~3k |
| `site_hourly.parquet` | Human views per hour for 8 weeks, five languages (en, de, ja, es, fr) | ~6.7k |
| `top_daily.parquet` | Top 100 English articles for each of the last 365 days | ~36k |
| `dump/pageviews-*.gz` | One raw hour of every Wikimedia project: ~7M lines of text | ~7M |

Source: [Wikimedia Pageviews API](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/)
and [pageview dumps](https://dumps.wikimedia.org/other/pageviews/), public, no account.

## Answers

**raw.py**

1. **Malformed lines:**
2. **Missing days:**
3. **Median vs mean:**
4. **Three spikes:**
5. **Weekly rhythm:**
6. **Bots:**

**build.py**

1. **Size and gaps:**
2. **Bots:**
3. **Cycles:**
4. **Spikes:**
5. **The regulars:**
6. **Business framing:**
7. **Tools:**

## Findings

## Thoughts

## Trade-offs

## Mistakes

## Lessons learned
