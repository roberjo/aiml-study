# aiml-study

A self-paced recreation of the UT Austin McCombs / Great Learning PG Program in AI & ML:
23 weeks, Nov 2026 → Apr 2027, from EDA to deployed agentic systems, with the banking-relevant
pieces the course skips (model risk management, MLOps, monitoring).

- **Curriculum:** [docs/Self-Study AI ML Program.md](docs/Self-Study%20AI%20ML%20Program.md)
- **Method, stack, and signature builds:** [docs/plan.md](docs/plan.md)
- **LinkedIn series (one post per assignment):** [posts/](posts/)
- **Tracker:** [AI/ML Study project board](https://github.com/users/roberjo/projects/1), one issue per week

## Quick start

```bash
uv sync                      # Python 3.12 env with the Course 1 stack
uv run marimo edit           # reactive notebooks
uv sync --group ml           # add the ML stack (from W4)
cp .env.example .env         # API keys, never committed
```

## Progress

| Phase | Weeks | Signature build | Status |
|---|---|---|---|
| Pre-work | W1 | Repo + environment | In progress |
| Python for AI | W2–3 | Living Lab (interactive EDA) | — |
| Predictive modeling | W4–9 | **Project 1:** Fraud detection + model card | — |
| GenAI for NLP | W10–15 | **Project 2:** Reg Z policy assistant | — |
| Agentic AI | W16–19 | **Project 3:** Helpdesk copilot | — |
| Deploying AI | W20–23 | **Capstone** | — |

## Layout

```
src/aiml/      shared helpers (data, eval, tracking, LLM client)
weeks/         one folder per week
projects/      the four projects + capstone
docs/          curriculum and plan
posts/         LinkedIn series: plan, voice guide, drafts
data/          gitignored; re-downloaded by scripts
```

All data is public or synthetic. Nothing from work goes in this repo.
