"""Download W2 data: Wikipedia pageviews from the Wikimedia REST API.

    uv run python weeks/w02-eda/get_data.py           # API data, ~2-3 minutes
    uv run python weeks/w02-eda/get_data.py --dump    # also one raw hourly dump file (~50 MB)

Writes Parquet files to data/w02/. Re-running skips files that already exist (delete one to
refresh it). No account needed; Wikimedia asks for a descriptive User-Agent, which is set below.
"""

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta

import polars as pl

from aiml import DATA

OUT = DATA / "w02"
API = "https://wikimedia.org/api/rest_v1/metrics/pageviews"
HEADERS = {"User-Agent": "aiml-study/0.1 (https://github.com/roberjo/aiml-study; learning project)"}

# A mix of topics with very different shapes: seasonal, weekly (school/work), one-off events,
# and steady background. Titles must match English Wikipedia exactly (underscores for spaces).
ARTICLES = {
    "seasonal": ["Halloween", "Christmas", "Thanksgiving", "Daylight_saving_time", "Leap_year"],
    "school_work": ["Mathematics", "Linear_algebra", "Python_(programming_language)", "Excel"],
    "events": [
        "Super_Bowl",
        "Solar_eclipse_of_April_8,_2024",
        "2024_Summer_Olympics",
        "2024_United_States_presidential_election",
        "Pope_Francis",
        "Pope_Leo_XIV",
    ],
    "pop_culture": ["Taylor_Swift", "Oppenheimer_(film)", "Wicked_(2024_film)", "Squid_Game"],
    "tech_money": ["ChatGPT", "Nvidia", "Bitcoin", "Artificial_intelligence"],
    "evergreen": ["Wikipedia", "Main_Page", "United_States", "Deaths_in_2025"],
}
AGENTS = ["user", "automated", "spider"]  # human, bots pretending to be human, declared crawlers
PROJECTS = ["en.wikipedia", "de.wikipedia", "ja.wikipedia", "es.wikipedia", "fr.wikipedia"]

START = date(2024, 1, 1)
END = date.today().replace(day=1) - timedelta(days=1)  # last day of the previous full month


def fetch(path: str, retries: int = 4) -> dict | None:
    """GET one API path. Returns None on 404 (no data / bad title); retries on 429 and 5xx."""
    url = f"{API}/{path}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            raise
    return None


def ymd(d: date) -> str:
    return d.strftime("%Y%m%d")


def per_article() -> pl.DataFrame:
    rows, missing = [], []
    for topic, titles in ARTICLES.items():
        for title in titles:
            for agent in AGENTS:
                t = urllib.parse.quote(title, safe="")
                data = fetch(
                    f"per-article/en.wikipedia/all-access/{agent}/{t}/daily/{ymd(START)}/{ymd(END)}"
                )
                if data is None:
                    missing.append(f"{title} ({agent})")
                    continue
                for item in data["items"]:
                    rows.append(
                        {
                            "date": datetime.strptime(item["timestamp"][:8], "%Y%m%d").date(),
                            "topic": topic,
                            "article": title,
                            "agent": agent,
                            "views": item["views"],
                        }
                    )
    if missing:
        print(f"  no data for {len(missing)}: {', '.join(missing)}")
    return pl.DataFrame(rows)


def aggregate(granularity: str, projects: list[str], agents: list[str], start, end) -> pl.DataFrame:
    fmt = "%Y%m%d%H"
    rows = []
    for project in projects:
        for agent in agents:
            data = fetch(
                f"aggregate/{project}/all-access/{agent}/{granularity}/"
                f"{start.strftime(fmt)}/{end.strftime(fmt)}"
            )
            for item in (data or {}).get("items", []):
                rows.append(
                    {
                        "timestamp": datetime.strptime(item["timestamp"], fmt),
                        "project": project,
                        "agent": agent,
                        "views": item["views"],
                    }
                )
    return pl.DataFrame(rows)


def top_daily(days: int = 365, keep: int = 100) -> pl.DataFrame:
    rows = []
    for i in range(days):
        d = END - timedelta(days=i)
        data = fetch(f"top/en.wikipedia/all-access/{d:%Y/%m/%d}")
        for item in (data or {}).get("items", []):
            for a in item["articles"][:keep]:
                rows.append(
                    {"date": d, "rank": a["rank"], "article": a["article"], "views": a["views"]}
                )
        if i % 60 == 0:
            print(f"  top articles: {i}/{days} days")
    return pl.DataFrame(rows)


def raw_dump() -> None:
    """One hour of the raw pageview dump: every project, every page, as space-separated text."""
    when = datetime.combine(END, datetime.min.time()).replace(hour=12)
    name = f"pageviews-{when:%Y%m%d-%H}0000.gz"
    dest = OUT / "dump" / name
    if dest.exists():
        print(f"  skip {dest.name} (exists)")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://dumps.wikimedia.org/other/pageviews/{when:%Y/%Y-%m}/{name}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=300) as resp, open(dest, "wb") as f:
        while chunk := resp.read(1 << 20):
            f.write(chunk)
    print(f"  wrote {dest.relative_to(DATA.parent)} ({dest.stat().st_size / 1e6:.0f} MB)")


def save(name: str, make) -> None:
    path = OUT / f"{name}.parquet"
    if path.exists():
        print(f"skip {name} (exists)")
        return
    t0 = time.perf_counter()
    print(f"fetching {name} ...")
    df = make()
    df.write_parquet(path)
    print(
        f"  wrote {path.relative_to(DATA.parent)}: {df.height:,} rows in {time.perf_counter() - t0:.0f}s"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dump", action="store_true", help="also download one raw dump hour")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"date range {START} to {END}")

    save("articles_daily", per_article)
    # Whole-site daily totals by agent: the bot-vs-human question at scale.
    save(
        "site_daily",
        lambda: aggregate(
            "daily",
            ["en.wikipedia"],
            AGENTS,
            datetime.combine(START, datetime.min.time()),
            datetime.combine(END, datetime.min.time()),
        ),
    )
    # Hourly human traffic for the last 8 full weeks, five languages: daily and weekly cycles.
    hourly_end = datetime.combine(END, datetime.min.time()).replace(hour=23)
    save(
        "site_hourly",
        lambda: aggregate(
            "hourly", PROJECTS, ["user"], hourly_end - timedelta(weeks=8, hours=-1), hourly_end
        ),
    )
    save("top_daily", top_daily)
    if args.dump:
        print("fetching raw dump ...")
        raw_dump()


if __name__ == "__main__":
    main()
