# W2 log

A dated, running record of what was done this week, what was decided and why, and what broke.
Newest entries at the bottom. The capture headings in [README.md](README.md) are the distilled
version; this is the raw trail.

## 2026-10-30 · Setup

**Done**
- Scaffolded `weeks/w02-eda/`: `get_data.py`, `raw.py`, `build.py`, `README.md`, this log.
- Ran `get_data.py --dump`: 3 min 34 s total. 27 of 27 article titles found.

  | File | Rows | Time |
  |---|---|---|
  | `articles_daily.parquet` | 79,947 | 35 s (81 API calls) |
  | `site_daily.parquet` | 3,012 | 1 s |
  | `site_hourly.parquet` | 6,720 | 2 s |
  | `top_daily.parquet` | 36,200 (362 of 365 days) | 163 s (365 calls) |
  | `dump/pageviews-20260930-120000.gz` | 6,981,457 lines, 64 MB | ~10 s |

- Checked both notebooks end to end with throwaway reference solutions kept outside the repo:
  all 7 raw checks pass; every build.py chart and your-turn cell renders. Solutions deleted.
- `ruff check`, `ruff format`, `marimo check`: clean.

**Decisions**
- **Dataset:** Wikipedia pageviews instead of the course's NYC taxi data (decided earlier).
  Same skills, but the spikes have stories, and bot traffic gives a real data-quality problem.
- **Raw pass reads Parquet with `pyarrow` into a list of dicts.** pyarrow is just the file
  reader; everything after that is plain Python, so no dataframe library sneaks in.
- **Checks use small made-up inputs with known answers** (a planted-spike series, hand-computed
  medians) instead of comparing against a library call, so the checks don't give away the solution.
- **Spike detector: median + MAD over the previous 28 days, threshold 10.** Mean and standard
  deviation get dragged by the spikes themselves; a high threshold keeps weekly rhythm from firing.
- **build.py mixes worked examples with YOUR TURN stubs** (A: missing days, B: bot share,
  C: Polars spikes, D: one-day wonders in SQL). Worked examples teach the idiom; stubs make
  me use it.
- **Polars + DuckDB + Altair as the framework pass,** with pandas covered by the book and Kaggle
  Learn. Polars expressions and DuckDB SQL are where the modern stack is going; pandas is what
  most examples online use.
- **Top-articles pull limited to 365 days and the top 100 per day** to keep the fetch under
  3 minutes and polite to the API.

**Things noticed while profiling (turned into questions, not answers)**
- The API returns *no row* for zero-view days: `Pope_Leo_XIV` is missing 348 days and
  `Deaths_in_2025` 111. Missing ≠ zero ≠ didn't exist, and the mean changes depending on which.
- On these 27 articles, `automated` views (52%) outnumber humans (42%).
- `Excel` gets ~21 human views a day. Probably not the page I meant to pick.
- Hourly peaks in UTC: en/de/fr at 19:00, es at 20:00, ja at 12:00.
- `.xxx` and `.xyz` sat in the daily top 10 for 152 and 30 days.
- Mobile beats desktop in the raw dump: `en.m` 4.5M views that hour vs `en` 3.0M.
- DuckDB parsed the 7M-line dump in 0.9 s with zero rejected lines.

**Problems**
- Polars gotcha found while testing YOUR TURN C: when MAD is 0, `0 / 0` gives NaN, and Polars
  treats `NaN > 10` as true, so flat stretches show up as hundreds of fake spikes. Added a hint
  to the stub rather than the fix.
- 3 of 365 days are missing from `top_daily` (362 returned). Not investigated yet.

**Next**
- Learn: book chapters 5–9, Kaggle Pandas and Data Visualization, crash course Numerical data.
- Raw pass, then framework pass, then the questions.
