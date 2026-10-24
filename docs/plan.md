# Build Plan — how to study this *and* learn how it's built

The [program doc](./Self-Study%20AI%20ML%20Program.md) is the **what** (23 weeks, Nov 2 2026 → Apr 5 2027).
This is the **how**: the learning method, the tooling stack, and the five signature builds that turn
a pile of notebooks into a portfolio that looks like it came from a top ML platform team.

> `study-plan.md` is the earlier 10-module tracker. The 23-week program supersedes it; the module
> order is the same, so nothing there is lost.

---

## 1. The learning method: Raw → Framework → Product

Every topic gets built three times. This is how you learn *how things are built*, not just how to call them.

| Pass | What you do | Example (W12 RAG) |
|---|---|---|
| **1 · Raw** | Implement the core idea in ~100 lines of NumPy / plain Python / the bare API. No frameworks. | Cosine similarity over embeddings in a NumPy array; stuff top-k chunks into a Claude prompt. |
| **2 · Framework** | Rebuild with the industry tool. Diff it against your raw version — what did the framework hide? | Chroma + LangChain retriever. Read the source of the one class you use most. |
| **3 · Product** | Wrap it in an eval, a tracker, and an interface someone else could use. | Eval harness (hit rate, faithfulness) + a citations UI + deployed endpoint. |

Raw-pass ladder across the program:

| Week | Raw build | Then the framework |
|---|---|---|
| W4 | Linear regression via normal equations + gradient descent in NumPy | `sklearn.linear_model` |
| W5 | A decision tree with Gini splits, recursive | `DecisionTreeClassifier` |
| W6 | Gradient boosting with stumps (10 lines in a loop) | XGBoost / LightGBM |
| W7 | micrograd → a 2-layer MLP with your own autograd | Keras 3 (PyTorch backend) |
| W10 | Karpathy's char-level GPT | Hugging Face `transformers` |
| W12 | NumPy vector search | Chroma |
| W16 | The agent loop: `while stop_reason == "tool_use"` against an LLM API | LangGraph |
| W17 | An MCP server over stdio with the official SDK, no helpers | FastMCP-style decorators |

**Rule from the program doc stays sacred:** Claude can write the code; *you* write the evaluation.

---

## 2. The stack

Chosen for being current, fast, and the things a Staff-level reviewer recognizes.

| Layer | Tool | Why it's here |
|---|---|---|
| Env & deps | **uv** (+ `pyproject.toml`, dependency groups per course) | Reproducible in seconds; one lockfile for the whole repo |
| Lint/format | **ruff** | One tool, instant |
| Notebooks | **marimo** (primary), Jupyter for Colab weeks | Reactive, stored as `.py` (clean git diffs), runs as an app, exports to WASM so readers can run your EDA *in their browser* |
| Data | **DuckDB + Polars**, pandas for compatibility | NYC TLC is tens of GB of Parquet — query it in place with DuckDB SQL instead of loading it |
| Viz | **Altair** (declarative, interactive), Plotly, seaborn for quick looks | Charts that are tooltipped and linked, not static PNGs |
| Classic ML | scikit-learn, XGBoost/LightGBM, **SHAP** | SHAP gives you the explainability story banks require |
| Deep learning | **Keras 3 on PyTorch**, Colab / Modal for GPU | Satisfies the course's TF/Keras while learning the PyTorch ecosystem |
| Tracking | **MLflow** (local server) | Every run logged: params, metrics, artifacts, model registry. This is the MLOps gap the course skips |
| LLMs | **Free tiers only**: Gemini (default) and Groq via one OpenAI-compatible client (`src/aiml/llm.py`); **DSPy** | $0 budget. DSPy turns prompts into optimizable programs |
| RAG | sentence-transformers, **Chroma**, a reranker | Matches the course; swap in pgvector later if you want |
| Agents | Raw loop → **LangGraph**, **MCP** | Course tools, built from the protocol up |
| Evals & tracing | **Inspect AI** or promptfoo for eval suites, **Langfuse** or **Arize Phoenix** (self-hosted, Docker) for traces | Open-source replacements for LangSmith; trace viewers look great in a demo |
| Serving | **FastAPI** + Pydantic, Docker | Typed contracts, OpenAPI docs for free |
| Interfaces | Streamlit for quick tools; **Next.js + shadcn/ui** for the showcase apps; marimo apps for interactive write-ups | Streamlit is what everyone ships — the polished front ends are what sets you apart |
| Write-ups | **Quarto** → GitHub Pages | Project reports, model cards, and design docs published as one site |
| Infra | Terraform, AWS (Lambda / ECS / Bedrock), GitHub Actions | Per the program doc's W21 |
| Monitoring | **Evidently** | Data and prediction drift reports for the capstone |
| Pair & mentor | Claude Code with `CLAUDE.md` + a `/review-project` skill | The written-review rubric from the program doc, one command away |

---

## 3. Repo architecture

```
aiml-study/
├── README.md               progress tracker + portfolio index
├── CLAUDE.md               house rules for Claude (incl. "don't write my evals")
├── pyproject.toml / uv.lock
├── src/aiml/               shared package — grows each week
│   ├── data.py             dataset download + caching
│   ├── evaluate.py         metrics, plots, cost-of-error tables
│   ├── tracking.py         MLflow helpers
│   └── llm.py              one client for free LLM providers
├── weeks/wNN-topic/        one folder per week: notebook(s), README, get_data.py
├── projects/               the 4 projects + capstone, each a deployable unit
├── site/                   Quarto site (write-ups, model cards, design docs)
├── docs/                   program source docs + this plan
└── .claude/skills/         review-project rubric
```

The `src/aiml` package is the quiet win: by W23 you've built a small internal ML platform
(data, eval, tracking, LLM client), the same way a real team would.

---

## 4. Five signature builds

These are the "stunning" parts: each one turns a course project into something you'd demo in an interview.

### ① Living Lab — interactive EDA you can run in the browser (W2–W3)
marimo notebooks over NYC TLC (DuckDB on Parquet) and credit eligibility, exported to **WASM** and
embedded in the Quarto site. Readers drag a slider (hour of day, borough) and the Altair charts
re-render live, with no server involved. The W3 "five findings" becomes a scrollytelling page.

### ② Fraud Risk Console — bank-grade model governance (W9 → W20)
FastAPI scoring service + a **Next.js/shadcn** dashboard:
- PR curve with a **threshold slider wired to dollars**: false-positive review cost vs. fraud loss, live.
- Per-transaction **SHAP waterfall** ("why was this flagged?").
- Model card and an **SR 11-7-style validation report** generated from MLflow run data.
- Champion/challenger: gradient boosting vs. neural net, side by side.

This is the piece no bootcamp grad has, and it speaks directly to Principal/Staff roles in banking.

### ③ Reg Z Copilot — a RAG assistant you can audit (W12–W15)
Chat on the left, **evidence panel** on the right: every answer cites the CFR section, shows the
retrieved chunks with scores, and highlights the sentences used. A second tab is the **eval dashboard**:
retrieval hit rate, faithfulness, refusal accuracy, $/query, run over run. Guardrail tests
run in **CI**, so a prompt change that breaks refusals fails the PR.

### ④ Agent Flight Recorder — watch agents think (W16–W19)
Helpdesk copilot on LangGraph, with every step traced to self-hosted **Langfuse/Phoenix**. The UI
shows the graph live as it executes (classify → retrieve → draft → escalate?), with the trace
tree beside it. Includes your MCP server exposing the policy checker to Claude Desktop/Claude Code,
which makes for a good demo: ask Claude to audit an expense report, and it calls *your* tool.

### ⑤ Capstone — shipped like production (W22–W23)
Design doc first (Quarto), then Terraform → AWS, GitHub Actions CI/CD with an **eval gate**,
Evidently drift report on a schedule, cost and latency budget dashboard, a 5-minute demo video.

### The portfolio site that ties it together
A Quarto (or Next.js) site on GitHub Pages: a landing page with your progress timeline, each project
as a card linking to write-up, live demo, model card, and code. This is what goes on the resume.

---

## 5. How to run each week

The program doc's rhythm, with tooling attached:

| When | What | Tooling |
|---|---|---|
| Weeknight 1 (90m) | Lecture/reading; take notes in the week's README | — |
| Weeknight 2 (90m) | **Raw pass** of the week's core idea | marimo notebook |
| Saturday (4h) | **Framework + product pass** on the build | uv, MLflow, Claude Code |
| Sunday (15m) | Commit, tick the box in README, 3 lines on what failed | `git`, `/review-project` on project weeks |

Per-week folder template:

```
weeks/w04-regression/
├── README.md        goal · reading · findings · what failed
├── get_data.py      reproducible download
├── raw.py           marimo: from-scratch implementation
└── build.py         marimo: framework version + eval
```

---

## 6. Phased tooling rollout

Don't install everything on day one. Each course adds one layer:

| Phase | Weeks | New tooling | Signature build |
|---|---|---|---|
| Foundation | W1–3 | uv, ruff, marimo, DuckDB, Altair, Quarto | ① Living Lab |
| ML platform | W4–9 | scikit-learn, XGBoost, SHAP, MLflow, Keras 3 | ② Fraud console (models) |
| GenAI | W10–15 | Gemini/Groq free tiers, DSPy, Chroma, Inspect/promptfoo, CI evals | ③ Reg Z Copilot |
| Agents | W16–19 | LangGraph, MCP, Langfuse/Phoenix (Docker) | ④ Flight Recorder |
| Production | W20–23 | FastAPI, Docker, Next.js, Terraform, AWS, Evidently | ② console UI + ⑤ Capstone |

---

## 7. Before Nov 2 (this week)

- [x] Repo scaffold, uv env, ruff, `.gitignore`, `CLAUDE.md`, review skill
- [ ] Create the GitHub repo and push
- [ ] Kaggle + Hugging Face accounts; free Gemini and Groq API keys in `.env`
- [ ] `brew install --cask quarto`
- [ ] Open `weeks/w01-setup/` and do the marimo tutorial: `uv run marimo tutorial intro`
