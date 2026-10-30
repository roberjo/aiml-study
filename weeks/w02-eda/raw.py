import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="W2 · EDA by hand")

with app.setup:
    import statistics
    from datetime import date, timedelta

    import marimo as mo
    import matplotlib.pyplot as plt
    import pyarrow.parquet as pq

    from aiml import DATA


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # W2 · EDA by hand: what is the internet paying attention to?

    Raw pass. Before pandas or Polars is allowed in, write the operations they do for you:
    parse messy text, summarize a column, group and sum, fill gaps, and find spikes.

    **Data:** daily English Wikipedia pageviews for 27 articles since Jan 2024, split by who
    viewed them: `user` (humans), `automated` (bots pretending to be human), and `spider`
    (declared crawlers). Run `uv run python weeks/w02-eda/get_data.py` first.

    **Rules:** plain Python only inside your functions: loops, lists, dicts, `datetime`, and
    `statistics.median` if you want it. No pandas, Polars, DuckDB, or NumPy.
    Checks run on small made-up inputs; the plots at the bottom run your code on the real data.

    Run with `uv run marimo edit weeks/w02-eda/raw.py`.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1 · Parse a line of the raw dump

    Wikimedia's hourly dump is a 7-million-line text file, one page per line:
    `project title views bytes`, e.g. `en.m Taylor_Swift 1234 0`.
    Real data is messy. Decide what counts as malformed and return `None` for it.
    """)
    return


@app.function
def parse_line(line):
    """'en Main_Page 123 0' -> {'project': 'en', 'title': 'Main_Page', 'views': 123}.

    Return None for a malformed line: wrong number of fields, views that aren't a
    non-negative whole number, or an empty line. Hint: str.split() and str.isdigit().
    """
    raise NotImplementedError


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2 · Summarize a column

    Missing values are `None`. Skip them, but count them: "how much is missing" is the first EDA question.
    """)
    return


@app.function
def describe(xs):
    """Return {'count', 'missing', 'mean', 'median', 'std', 'min', 'max'} for a list with Nones.

    count is the non-None values. std is the *sample* standard deviation: divide by count - 1,
    not count. (pandas and Polars do it that way; NumPy divides by count. Remember this.)
    Write mean and std yourself; statistics.median is fine for the median.
    """
    raise NotImplementedError


@app.function
def group_sum(rows, key, value="views"):
    """Sum row[value] for each distinct row[key]. rows is a list of dicts. Returns a dict.

    group_sum([{'a': 'x', 'views': 1}, {'a': 'x', 'views': 2}], 'a') -> {'x': 3}
    This is GROUP BY. Every dataframe library is built around it.
    """
    raise NotImplementedError


@app.function
def weekday_means(dates, values):
    """Average value for each weekday. Returns a list of 7 floats: Monday first, Sunday last.

    Hint: date.weekday() is 0 for Monday. Keep a running total and a count per weekday.
    """
    raise NotImplementedError


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3 · Time series: gaps and spikes
    """)
    return


@app.function
def fill_missing_days(dates, values):
    """Return (all_dates, all_values) covering every day from min(dates) to max(dates).

    Days that aren't in the input get 0. The input may not be sorted. Why does this exist?
    Find out in question 2.
    Hint: a dict from date to value, then walk from the first day to the last with timedelta(days=1).
    """
    raise NotImplementedError


@app.function
def rolling_median(xs, window):
    """Trailing rolling median: out[i] = median of xs[i - window + 1 .. i], inclusive.

    The first window - 1 entries don't have a full window yet: make them None.
    Returns a list the same length as xs.
    """
    raise NotImplementedError


@app.function
def find_spikes(xs, window=28, k=10):
    """Indexes i where xs[i] is a spike compared to the `window` days *before* it.

    Robust z-score: (xs[i] - m) / (1.4826 * mad) > k, where over the previous `window` values,
    m is their median and mad is the median of |value - m| (median absolute deviation).
    1.4826 scales MAD to match a standard deviation for normal data.
    If mad is 0 (a flat stretch), skip that day.

    Why median and MAD instead of mean and standard deviation? That's question 3.
    """
    raise NotImplementedError


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Checks
    """)
    return


@app.cell(hide_code=True)
def _():
    _d0 = date(2026, 1, 5)  # a Monday
    _days = [_d0 + timedelta(days=i) for i in range(14)]
    _xs = [3, None, 1, 4, 1, 5, None, 9]
    _ok = [x for x in _xs if x is not None]

    # Flat-ish series with two planted spikes at index 50 and 90.
    _base = [1000 + (i * 37) % 61 - 30 for i in range(120)]
    _spiky = list(_base)
    _spiky[50] *= 5
    _spiky[90] *= 3

    def _describe_ok():
        d = describe(_xs)
        want = {
            "count": 6,
            "missing": 2,
            "mean": sum(_ok) / 6,
            "median": 3.5,
            "std": statistics.stdev(_ok),
            "min": 1,
            "max": 9,
        }
        return all(abs(d[k] - v) < 1e-9 for k, v in want.items())

    def _fill_ok():
        ds, vs = fill_missing_days([date(2026, 1, 4), date(2026, 1, 1)], [7, 5])
        return ds == [date(2026, 1, d) for d in range(1, 5)] and vs == [5, 0, 0, 7]

    def _rolling_ok():
        return rolling_median([5, 1, 3, 10, 2, 8], 3) == [None, None, 3, 3, 3, 8]

    _checks = {
        "parse_line": lambda: (
            parse_line("en Main_Page 123 0")
            == {"project": "en", "title": "Main_Page", "views": 123}
            and parse_line("de.m Berlin 5 0\n")
            == {"project": "de.m", "title": "Berlin", "views": 5}
            and all(
                parse_line(bad) is None
                for bad in [
                    "",
                    "en Main_Page",
                    "en Main_Page abc 0",
                    "en Two words 5 0",
                    "en X -3 0",
                ]
            )
        ),
        "describe": _describe_ok,
        "group_sum": lambda: (
            group_sum(
                [{"a": "x", "views": 1}, {"a": "y", "views": 10}, {"a": "x", "views": 2}], "a"
            )
            == {"x": 3, "y": 10}
        ),
        "weekday_means": lambda: (
            weekday_means(_days, list(range(14))) == [3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
        ),
        "fill_missing_days": _fill_ok,
        "rolling_median": _rolling_ok,
        "find_spikes": lambda: find_spikes(_spiky) == [50, 90],
    }

    def _status(check):
        try:
            return "✅" if check() else "❌ wrong answer"
        except NotImplementedError:
            return "⏳ not started"
        except Exception as e:  # typos, wrong types, etc.
            return f"❌ {type(e).__name__}: {e}"

    _rows = "\n".join(f"| `{name}` | {_status(c)} |" for name, c in _checks.items())
    mo.md(f"| Function | Status |\n|---|---|\n{_rows}")
    return


@app.function
def attempt(f, *args, **kwargs):
    """Call f, returning None if it isn't implemented yet (so the plots can wait for you)."""
    try:
        return f(*args, **kwargs)
    except NotImplementedError:
        return None


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Your code on the real data
    """)
    return


@app.cell
def _():
    _path = DATA / "w02" / "articles_daily.parquet"
    mo.stop(not _path.exists(), mo.md("Run `uv run python weeks/w02-eda/get_data.py` first."))
    rows = pq.read_table(_path).to_pylist()  # a plain list of dicts: no dataframe allowed yet
    series = {}  # article -> (dates, views), human traffic only
    for _r in rows:
        if _r["agent"] == "user":
            _d, _v = series.setdefault(_r["article"], ([], []))
            _d.append(_r["date"])
            _v.append(_r["views"])
    pick = mo.ui.dropdown(sorted(series), value="Taylor_Swift", label="Article")
    mo.vstack([mo.md(f"Loaded **{len(rows):,}** rows."), pick])
    return pick, rows, series


@app.cell
def _(rows):
    _by_agent = attempt(group_sum, rows, "agent")
    _by_article_human = attempt(group_sum, [r for r in rows if r["agent"] == "user"], "article")
    mo.stop(_by_agent is None, mo.md("_Implement `group_sum` to see who is reading._"))
    _total = sum(_by_agent.values())
    _lines = [f"| {a} | {v:,} | {v / _total:.0%} |" for a, v in sorted(_by_agent.items())]
    _top = sorted(_by_article_human.items(), key=lambda kv: -kv[1])[:5]
    mo.md(
        "**Views by agent, all 27 articles**\n\n| agent | views | share |\n|---|---|---|\n"
        + "\n".join(_lines)
        + "\n\n**Most-read by humans:** "
        + ", ".join(f"{a} ({v:,})" for a, v in _top)
    )
    return


@app.cell
def _(pick, series):
    _dates, _views = series[pick.value]
    _stats = attempt(describe, _views)
    _filled = attempt(fill_missing_days, _dates, _views)
    _lines = [f"**{pick.value}**: {len(_dates):,} days with data"]
    if _stats:
        _lines.append(
            f"mean {_stats['mean']:,.0f} · median {_stats['median']:,.0f} · "
            f"std {_stats['std']:,.0f} · max {_stats['max']:,}"
        )
    if _filled:
        _full = describe(_filled[1]) if _stats else None
        _gap = len(_filled[0]) - len(_dates)
        _lines.append(f"after filling gaps: {len(_filled[0]):,} days ({_gap:,} were missing)")
        if _full:
            _lines.append(f"mean with the gaps filled: {_full['mean']:,.0f}")
    mo.md("  \n".join(_lines))
    return


@app.cell
def _(pick, series):
    _dates, _views = series[pick.value]
    _filled = attempt(fill_missing_days, _dates, _views)
    _fig, (_ax, _bx) = plt.subplots(1, 2, figsize=(11, 3.4), width_ratios=[3, 1])
    _ds, _vs = _filled or (_dates, _views)
    _ax.plot(_ds, _vs, lw=0.8, color="steelblue")
    _ax.set(title=f"{pick.value}: daily human views", yscale="log")
    _spikes = attempt(find_spikes, _vs) if _filled else None
    if _spikes:
        _ax.scatter(
            [_ds[i] for i in _spikes], [_vs[i] for i in _spikes], color="crimson", s=14, zorder=3
        )
        for _i in sorted(_spikes, key=lambda i: -_vs[i])[:3]:
            _ax.annotate(
                f"{_ds[_i]:%Y-%m-%d}",
                (_ds[_i], _vs[_i]),
                fontsize=8,
                xytext=(4, 4),
                textcoords="offset points",
            )
    _wk = attempt(weekday_means, _dates, _views)
    if _wk:
        _bx.bar(list("MTWTFSS"), _wk, color="steelblue")
        _bx.set(title="mean by weekday")
    else:
        _bx.text(0.5, 0.5, "implement weekday_means", ha="center", transform=_bx.transAxes)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Red dots appear once `fill_missing_days` and `find_spikes` both work; the three biggest are labelled.

    ## Questions (answer in the README)

    1. **Malformed lines:** which cases did you decide to reject, and why? What did you assume
       about valid data that the dump might break?
    2. **Missing days:** the API returns *no row* for a day with zero views. Pick `Pope_Leo_XIV`
       and compare the mean before and after `fill_missing_days`. Which number is honest, and
       for what question? What does "missing" actually mean for this article?
    3. **Median vs mean:** why does `find_spikes` use median and MAD instead of mean and standard
       deviation? (Think about what one 7-million-view day does to a 28-day standard deviation.)
    4. **Three spikes:** pick three red dots on three different articles. Look up the date and
       name the real-world event behind each. Did any spike surprise you?
    5. **Weekly rhythm:** which articles are busiest Monday to Friday and which on weekends?
       What does that say about who reads them, and why?
    6. **Bots:** from the agent table, what share of views on these 27 articles came from
       humans? Switch the dropdown to `Python_(programming_language)` and `Main_Page` and guess
       why bots love them. (`build.py` checks your guess.)
    """)
    return


if __name__ == "__main__":
    app.run()
