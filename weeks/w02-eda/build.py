import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="W2 · Wikipedia attention EDA")

with app.setup:
    import gzip
    import time

    import altair as alt
    import duckdb
    import marimo as mo
    import numpy as np
    import polars as pl
    from raw import describe, parse_line

    from aiml import DATA

    W02 = DATA / "w02"
    alt.data_transformers.disable_max_rows()


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # W2 · Framework pass: Wikipedia attention, with Polars, DuckDB, and Altair

    Same questions as `raw.py`, now with the tools you'd actually use. Each section has a
    **worked example** (read it, run it, change it) and a **your turn** cell (a stub that's
    `None` until you write it; its chart appears when you do).

    **Why these three tools?**

    - **Polars**: a dataframe library like pandas, but columnar, multi-threaded, and with a
      lazy mode that plans the whole query before running it. Its expressions
      (`pl.col("views").sum().over("article")`) read like the operation you mean.
    - **DuckDB**: SQL straight over Parquet and CSV files, no server, no loading step. When
      the data is bigger than memory, DuckDB streams it.
    - **Altair**: charts as data. You describe the encoding (x is date, color is agent) and it
      draws, with tooltips and selections for free.

    Pandas is still everywhere (the course uses it, and so do most examples online). Book
    chapters 5–9 cover it; try one of the your-turn cells in pandas too (`df.to_pandas()`).
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1 · How big is it, and what's missing?
    """)
    return


@app.cell
def _():
    mo.stop(not W02.exists(), mo.md("Run `uv run python weeks/w02-eda/get_data.py` first."))
    articles = pl.read_parquet(W02 / "articles_daily.parquet")
    site_daily = pl.read_parquet(W02 / "site_daily.parquet")
    site_hourly = pl.read_parquet(W02 / "site_hourly.parquet")
    top = pl.read_parquet(W02 / "top_daily.parquet")
    mo.md(
        "| table | rows | columns |\n|---|---|---|\n"
        + "\n".join(
            f"| `{n}` | {t.height:,} | {', '.join(t.columns)} |"
            for n, t in [
                ("articles", articles),
                ("site_daily", site_daily),
                ("site_hourly", site_hourly),
                ("top", top),
            ]
        )
    )
    return articles, site_daily, site_hourly, top


@app.cell
def _(articles):
    articles.describe()
    return


@app.cell
def _(articles):
    # Three tools, one column, three answers. Which one disagrees, and why? (Question 1.)
    _views = articles.filter(pl.col("agent") == "user")["views"]
    _mine = describe(_views.to_list()) if _views.len() else None
    mo.md(
        f"""
    Standard deviation of human daily views:

    - Polars `.std()`: **{_views.std():,.1f}**
    - NumPy `np.std()`: **{np.std(_views.to_numpy()):,.1f}**
    - your `describe()`: **{_mine["std"]:,.1f}**
    """
        if _mine
        else "_Implement `describe` in raw.py to compare._"
    )
    return


@app.cell
def _(articles):
    # Worked example: build a complete calendar so a missing day becomes an explicit 0.
    # Same idea as your fill_missing_days, done as a join: every (article, date) pair, then
    # left-join the real rows onto it.
    _human = articles.filter(pl.col("agent") == "user").select("date", "article", "views")
    _calendar = pl.DataFrame(
        {"date": pl.date_range(_human["date"].min(), _human["date"].max(), eager=True)}
    )
    human_daily = (
        _calendar.join(_human.select("article").unique(), how="cross")
        .join(_human, on=["date", "article"], how="left")
        .with_columns(missing=pl.col("views").is_null(), views=pl.col("views").fill_null(0))
        .sort("article", "date")
    )
    human_daily.head()
    return (human_daily,)


@app.cell
def _(human_daily):
    # YOUR TURN A: one row per article with how many days were missing and the first day
    # that has data. Sort by most missing.
    # Hint: human_daily.group_by("article").agg(
    #     pl.col("missing").sum().alias("missing_days"),
    #     pl.col("date").filter(~pl.col("missing")).min().alias("first_seen"),
    # )
    missing_days = None
    missing_days
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2 · Bots vs humans
    """)
    return


@app.cell
def _(site_daily):
    # Worked example: all of English Wikipedia, daily, stacked by agent.
    _weekly = site_daily.group_by_dynamic("timestamp", every="1w", group_by="agent").agg(
        pl.col("views").sum()
    )
    alt.Chart(_weekly).mark_area().encode(
        x=alt.X("timestamp:T", title=None),
        y=alt.Y("views:Q", title="weekly views", stack=True),
        color=alt.Color("agent:N", sort=["user", "spider", "automated"]),
        tooltip=["timestamp:T", "agent:N", alt.Tooltip("views:Q", format=",")],
    ).properties(width="container", height=260, title="English Wikipedia: who is reading?")
    return


@app.cell
def _(articles):
    # YOUR TURN B: bot share per article = (automated + spider) / all views.
    # Hint: articles.group_by("article", "agent").agg(pl.col("views").sum())
    #         .pivot(on="agent", index="article", values="views")
    #         .with_columns(bot_share=...)
    # Keep columns: article, user, automated, spider, bot_share.
    bot_share = None
    bot_share
    return (bot_share,)


@app.cell
def _(bot_share):
    mo.stop(bot_share is None, mo.md("_Chart appears when `bot_share` is filled in._"))
    alt.Chart(bot_share).mark_bar().encode(
        x=alt.X("bot_share:Q", axis=alt.Axis(format="%"), title="share of views from bots"),
        y=alt.Y("article:N", sort="-x", title=None),
        tooltip=[
            "article",
            alt.Tooltip("bot_share:Q", format=".1%"),
            alt.Tooltip("user:Q", format=","),
        ],
    ).properties(width="container", height=520)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3 · Daily and weekly cycles across languages
    """)
    return


@app.cell
def _(site_hourly):
    # Worked example: hour-of-day x weekday heatmap per language, in UTC.
    # Each project is divided by its own mean, so 1.0 = an average hour for that language.
    _cycle = (
        site_hourly.with_columns(
            hour=pl.col("timestamp").dt.hour(), weekday=pl.col("timestamp").dt.strftime("%a")
        )
        .group_by("project", "weekday", "hour")
        .agg(pl.col("views").mean())
        .with_columns(rel=pl.col("views") / pl.col("views").mean().over("project"))
    )
    alt.Chart(_cycle).mark_rect().encode(
        x=alt.X("hour:O", title="hour (UTC)"),
        y=alt.Y("weekday:N", sort=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], title=None),
        color=alt.Color("rel:Q", scale=alt.Scale(scheme="viridis"), title="vs avg hour"),
        tooltip=["project", "weekday", "hour", alt.Tooltip("rel:Q", format=".2f")],
    ).properties(width=360, height=140).facet(facet="project:N", columns=2)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4 · Spikes, the Polars way
    """)
    return


@app.cell
def _(human_daily):
    # YOUR TURN C: the robust z-score from raw.py's find_spikes, as Polars expressions.
    # Per article (.over("article")), over the previous 28 days (.shift(1) after the rolling):
    #   med   = rolling_median of views
    #   mad   = rolling_median of |views - med|   <- an approximation of true MAD; why?
    #   score = (views - med) / (1.4826 * mad)
    # Keep rows with score > 10. Columns: date, article, views, score.
    # Hint: pl.col("views").rolling_median(window_size=28).shift(1).over("article")
    # Then sanity-check the top of your result. Like raw.py, days where mad == 0 need
    # handling: what is 0 / 0 in Polars, and is it greater than 10?
    spikes = None
    spikes
    return (spikes,)


@app.cell
def _(human_daily):
    pick = mo.ui.dropdown(
        sorted(human_daily["article"].unique()), value="Taylor_Swift", label="Article"
    )
    pick
    return (pick,)


@app.cell
def _(human_daily, pick, spikes):
    _one = human_daily.filter(pl.col("article") == pick.value, pl.col("views") > 0)
    _line = (
        alt.Chart(_one)
        .mark_line(strokeWidth=1)
        .encode(
            x=alt.X("date:T", title=None),
            y=alt.Y("views:Q", scale=alt.Scale(type="log"), title="daily human views"),
            tooltip=["date:T", alt.Tooltip("views:Q", format=",")],
        )
    )
    _layers = [_line]
    if spikes is not None:
        _dots = (
            alt.Chart(spikes.filter(pl.col("article") == pick.value))
            .mark_circle(color="crimson", size=50)
            .encode(
                x="date:T",
                y="views:Q",
                tooltip=[
                    "date:T",
                    alt.Tooltip("views:Q", format=","),
                    alt.Tooltip("score:Q", format=".0f"),
                ],
            )
        )
        _layers.append(_dots)
    alt.layer(*_layers).properties(width="container", height=280, title=pick.value).interactive()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5 · The daily top 1,000, with SQL

    DuckDB can query a Polars dataframe by its Python variable name, or a Parquet file by path.
    """)
    return


@app.cell
def _(top):
    # Worked example: which articles live in the top 10?
    duckdb.sql("""
        SELECT article, count(*) AS days_in_top10, max(views) AS best_day
        FROM top
        WHERE rank <= 10
        GROUP BY article
        ORDER BY days_in_top10 DESC
        LIMIT 15
    """).pl()
    return


@app.cell
def _(top):
    # YOUR TURN D: "one-day wonders": articles that reached the top 10 on exactly one day.
    # Show the date and views, biggest first. These are your best spike candidates, and some
    # of the regulars above are not people at all. Write the SQL.
    one_day_wonders = None
    one_day_wonders
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6 · The raw dump: your loop vs DuckDB

    One hour of *every* Wikimedia project, ~7 million lines of text. Same race as W1: your
    `parse_line` in a Python loop against DuckDB's parallel C++ CSV reader.
    Needs `get_data.py --dump`.
    """)
    return


@app.cell
def _():
    dumps = sorted((W02 / "dump").glob("*.gz")) if (W02 / "dump").exists() else []
    race = mo.ui.run_button(label="Run the race (your loop takes a while)")
    mo.vstack([mo.md(f"Dump file: `{dumps[0].name}`" if dumps else "_No dump downloaded._"), race])
    return dumps, race


@app.cell
def _(dumps, race):
    mo.stop(not dumps or not race.value)
    _f = str(dumps[0])

    _t0 = time.perf_counter()
    _db = duckdb.sql(f"""
        SELECT project, sum(views) AS views, count(*) AS pages
        FROM read_csv('{_f}', delim=' ', header=false, quote='', escape='',
                      columns={{'project': 'VARCHAR', 'title': 'VARCHAR',
                                'views': 'BIGINT', 'bytes': 'BIGINT'}},
                      ignore_errors=true)
        GROUP BY project ORDER BY views DESC
    """).pl()
    _t_db = time.perf_counter() - _t0

    _t0 = time.perf_counter()
    _mine, _bad = {}, 0
    try:
        with gzip.open(_f, "rt", encoding="utf-8", errors="replace") as _fh:
            for _line in _fh:
                _p = parse_line(_line)
                if _p is None:
                    _bad += 1
                else:
                    _mine[_p["project"]] = _mine.get(_p["project"], 0) + _p["views"]
        _t_mine = time.perf_counter() - _t0
        _mine_msg = f"your loop: **{_t_mine:.1f} s**, {_bad:,} lines rejected · DuckDB: **{_t_db:.2f} s** · **{_t_mine / _t_db:.0f}×**"
    except NotImplementedError:
        _mine_msg = f"DuckDB: **{_t_db:.2f} s**. Implement `parse_line` to race it."
    mo.vstack([mo.md(_mine_msg), _db.head(15)])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Questions (answer in the README)

    1. **Size and gaps:** how many rows, articles, and days? Which articles have missing days,
       and what does "missing" mean for each (didn't exist yet? zero views? a renamed page?).
       Why did NumPy's standard deviation disagree with Polars and yours?
    2. **Bots:** which articles have the highest bot share, and what's your theory for each?
       Look closely at `Excel`: is it what you think it is? What would a model trained on
       `all-agents` views learn that one trained on `user` views wouldn't?
    3. **Cycles:** when does each language peak, in UTC? One of them is out of step with the
       rest. Why? What does the weekday pattern say about how people use Wikipedia?
    4. **Spikes:** find three spikes (from YOUR TURN C or D) and explain each with the
       real-world event behind it. How many did your Polars version find vs `find_spikes`
       in raw.py? If they differ, why?
    5. **The regulars:** some articles sit in the top 10 for months. Which ones are clearly not
       human attention, and how could you tell from this data alone?
    6. **Business framing:** you run capacity planning and caching for Wikipedia. Name three
       decisions this data supports (when to scale, what to cache, how much traffic is bots)
       and the one number you'd put on a dashboard for each.
    7. **Tools:** what did Polars or DuckDB make easy that was painful by hand? What did writing
       it by hand teach you that the library hides?
    """)
    return


if __name__ == "__main__":
    app.run()
