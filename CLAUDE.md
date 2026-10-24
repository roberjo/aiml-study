# aiml-study — notes for Claude

A personal AI/ML study repo. The goal is for the owner to **learn**, so optimize for understanding, not speed.

## Rules
- **Do not write evaluation code** (metrics, eval sets, judge prompts, test harnesses) unless explicitly asked. Review it, critique it, suggest what's missing — but the owner writes it.
- On "raw pass" files (`raw.py`), don't import the framework being learned (no sklearn in a from-scratch regression). Prefer hints over full solutions.
- Explain *why* when introducing a library feature or a modeling choice.
- LLM calls go through `aiml.llm` (free providers only: Gemini, Groq, Ollama). No paid APIs.
- Public or synthetic data only. Never add work data, credentials, or bank-internal references.

## Conventions
- uv for everything: `uv run`, `uv add` (`--group ml` etc. for course-specific deps). Python 3.12.
- Notebooks are marimo `.py` files unless a week needs Colab/Jupyter.
- Week folders: `weeks/wNN-topic/` with `README.md`, `get_data.py`, `raw.py`, `build.py`.
- Reusable code goes in `src/aiml/` once it's used in two weeks.
- Data goes in `data/` (gitignored). Large data: query Parquet with DuckDB rather than loading it all.
- `uv run ruff check . && uv run ruff format .` before committing.

See `docs/plan.md` for the method and stack, and `docs/Self-Study AI ML Program.md` for the curriculum.
