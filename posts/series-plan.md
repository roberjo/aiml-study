# Series plan

These are **starting angles**, not scripts. The real post comes from what actually happened that week;
if a better story emerges (it usually does), use it instead. Post the week after the build.

Formats: **T** text, **I** text + image/chart, **C** carousel (PDF), **V** short demo video.

| # | Week | Assignment | Planned angle | Trade-off to explore | Fmt |
|---|---|---|---|---|---|
| 0 | Kickoff | Course review + setup | I'm rebuilding a $3,950 AI/ML program in public for $0. What the fee really buys is accountability, not content | Structure + credential vs. cost + freedom | T |
| 1 | W1 | Math refresher, environment | Notebooks as code: why I picked reactive marimo notebooks over Jupyter, and what a matrix actually *does* to space | Familiar tools vs. reproducibility and clean diffs | I |
| 2 | W2 | Ride-sharing demand EDA | Stop loading data into memory: querying millions of taxi trips in place with DuckDB | pandas familiarity vs. DuckDB/Polars speed | I |
| 3 | W3 | Credit eligibility EDA | Charts aren't findings. Rewriting my EDA so a non-technical reader could act on it | Thoroughness vs. what a stakeholder will read | I |
| 4 | W4 | Insurance premium regression | Linear regression three ways (normal equation, gradient descent, sklearn) and what the library hides | Closed form vs. iterative; understanding vs. speed | I |
| 5 | W5 | Credit trees + classification metrics | 95% accuracy, useless model. Why accuracy lies on imbalanced data | Precision vs. recall when the cost is a rejected applicant | I |
| 6 | W6 | Ensembles, bike demand, maintenance | Gradient boosting in 10 lines, and why it still beats deep learning on tables | Interpretability vs. accuracy | I |
| 7 | W7 | Neural nets from scratch → Keras | I built backprop by hand. Here's the one idea that made it click | From-scratch time cost vs. depth of understanding | I |
| 8 | W8 | Break week | What I'd cut if I started over: an honest retro of the first 7 weeks | Consistency vs. burnout | T |
| 9 | W9 | **Project 1: fraud detection** | 0.17% fraud rate: putting a dollar cost on every error, and writing the model card nobody asks for until an auditor does | Neural net vs. gradient boosting; catch rate vs. analyst workload | C |
| 10 | W10 | LLMs, ticket categorization | Prompted LLM vs. a small fine-tuned classifier: when the boring model wins | Flexibility vs. cost, latency, consistency | I |
| 11 | W11 | GenAI evals, news sentiment | 100 hand-labeled examples taught me more than any prompt tip. Plus: letting DSPy rewrite my prompt | Eval effort vs. confidence; hand prompts vs. optimized | I |
| 12 | W12 | RAG over Regulation Z | Vector search in 20 lines of NumPy, then Chroma. Chunking mattered more than the database | Chunk size vs. retrieval precision | I |
| 13 | W13 | Guardrails | Testing refusals like unit tests: what my assistant should *not* answer | Safety vs. helpfulness (over-refusal is a failure too) | T |
| 14 | W14 | Break week | Halfway: $0 spent, what's working, what isn't | — | T |
| 15 | W15 | **Project 2: policy assistant** | Every answer cites its source, and here's how often it's actually faithful | Faithfulness vs. answer completeness; cost per query | C |
| 16 | W16 | Single agent, reimbursements | An agent loop is ~40 lines. Most problems don't need one | Agent autonomy vs. a deterministic workflow | I |
| 17 | W17 | MCP server | I built an MCP server. What the protocol actually is, minus the hype | Standard protocol vs. custom integration | V |
| 18 | W18 | Multi-agent + tracing | Multi-agent made my system worse until I could see the traces | Specialization vs. coordination overhead | I |
| 19 | W19 | **Project 3: helpdesk copilot** | The most important metric was how often it said "I don't know." Grading 20 traces by hand | Automation rate vs. escalation safety | C |
| 20 | W20 | FastAPI + Docker deploy | The notebook-to-service gap: what changed when real requests hit my model | Speed of shipping vs. production hygiene | I |
| 21 | W21 | AWS + Terraform + monitoring | Cost and latency budgets: designing for the bill, and watching for drift | Managed services vs. control; cost vs. latency | I |
| 22 | W22 | Capstone design doc | I wrote the design doc before the code. Here's what it caught | Upfront design vs. discovering by building | T |
| 23 | W23 | **Capstone + series retro** | 23 weeks, $0, one deployed system. What the $3,950 would and wouldn't have bought | Self-study vs. paid program, in hindsight | V |
