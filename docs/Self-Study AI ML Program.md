# Self-Study AI/ML Program

Oct 24, 2026 · @John Roberts

## Course review

The content is reproducible for free. The roughly $3,950 fee buys structure, weekly mentor time, and a Texas McCombs certificate, and the program is built for people without a coding background, so a working Python engineer would spend the first third on material he already has.

| Item | What the course offers |
| --- | --- |
| Provider | Great Learning, with a certificate of completion and CEUs from UT Austin McCombs ([program page](https://www.mygreatlearning.com/pg-program-online-artificial-intelligence-machine-learning)) |
| Length | 23 weeks online, 200+ hours of content |
| Format | Recorded faculty lectures, monthly live masterclasses, weekend live mentor sessions, a program manager |
| Curriculum | Pre-work; Python for AI; Predictive modeling with ML and neural nets; GenAI for NLP; Agentic AI; Deploying AI |
| Hands-on | 4 projects plus 30+ case studies |
| Tools | scikit-learn, TensorFlow, Hugging Face, ChromaDB, LangChain, LangGraph, LangSmith, DSPy, OpenAI API, Claude, MCP, Docker, Streamlit |
| Fee | About USD 3,950 per a third-party listing ([source](https://www.techinterview.org/bootcamp_directory/p/great-learning-ai-ml/)); the program page hides the fee behind a form |
| Next deadline | Applications close Oct 29, 2026 |

**Where it is strong**

- Current scope: RAG, evaluation, single- and multi-agent systems, MCP, and deployment, not just classic ML.
- Applied framing: every module ends in a business case study, several of them finance (fraud, credit eligibility, reimbursement, stock sentiment).

**Where it is thin, for you**

- Pre-work and Course 1 are Python and pandas basics.
- Math and statistics are light; it is a business-applications program, not an ML theory program.
- Deployment gets about 3 weeks. There is no real MLOps, monitoring, or model risk management, which is what a bank actually gates on.
- It publishes no placement or salary outcomes, and the certificate is non-credit executive education.

**Bottom line:** do it yourself and spend a fraction of the money on API credits. The plan below keeps the course's sequence and projects, compresses what you already know, and adds the banking-relevant pieces it skips.

## How this version works

Same 23 weeks, about 8–10 hours a week, starting Monday, Nov 2, 2026 and finishing the week of Apr 5, 2027.

**Weekly rhythm**

- Two weeknight sessions of 90 minutes: lectures and reading.
- One Saturday block of about 4 hours: the build. This replaces the course's weekend mentor session.
- Sunday, 15 minutes: commit, tick the week off below, write three lines on what didn't work.

**Setup (do before Week 1)**

- [ ] Personal laptop and personal accounts only. No work data, no work credentials, no bank systems.
- [ ] One GitHub repo, `aiml-selfstudy`, with a folder per week and a README per project.
- [ ] Python 3.12 with uv or conda, Jupyter in VS Code; Google Colab for free GPU time in the deep learning weeks.
- [ ] Kaggle and Hugging Face accounts for datasets and models.
- [ ] One LLM API key (Anthropic or OpenAI) with a hard monthly spend cap of about $20; Ollama with a small local model as the free fallback.

**Rules**

1. Every week ends in a commit, even a small one.
2. A project is done when it reports a metric on held-out data and has a one-page write-up: problem, data, approach, result, what failed.
3. Use Copilot or Claude to write code, but write the evaluation yourself. That is the skill the course calls "strategic judgement."
4. Two missed weeks in a row: use the next break week to catch up rather than skipping ahead.

Day-by-day tasks and the first step for each session: Daily assignments

## Week-by-week plan

The sequence matches the course module for module; tick each week off as you finish it. Dates are week start (Mondays).

### Pre-work (Week 1)

The course spends this on Python basics; you spend it on the math you'll lean on later.

- [ ] **W1 · Nov 2** — AI landscape plus a math refresher. Learn: [Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra) (chapters 1–7), [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course) intro modules. Build: repo scaffold and environment from the setup list.

### Course 1: Python for AI Solutions (Weeks 2–3)

- [ ] **W2 · Nov 9** — pandas, cleaning, EDA, plotting. Learn: [Python for Data Analysis, 3rd ed.](https://wesmckinney.com/book/) chapters 5–9 (skim what you know), [Kaggle Learn](https://www.kaggle.com/learn) Pandas and Data Visualization. Build: ride-sharing demand EDA.
- [ ] **W3 · Nov 16** — EDA as a business deliverable, AI-assisted analysis. Build: credit card eligibility EDA with five written findings a non-technical reader could act on.

### Course 2: Predictive Modeling with ML and Neural Networks (Weeks 4–9)

- [ ] **W4 · Nov 23** — Linear regression, train/test splits, cross-validation, regression metrics. Learn: [ISLP](https://www.statlearning.com/) chapters 2–3 and 5, [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html). Build: insurance premium prediction. (Thanksgiving week: aim for half.)
- [ ] **W5 · Nov 30** — Classification and decision trees; precision, recall, ROC and PR curves. Learn: ISLP chapters 4 and 8. Build: tree classifier on the credit eligibility data from W3.
- [ ] **W6 · Dec 7** — Ensembles (random forest, gradient boosting) and K-Means clustering. Learn: ISLP chapters 8 and 12, XGBoost or LightGBM quick-start. Build: bike demand forecast and predictive maintenance classifier.
- [ ] **W7 · Dec 14** — Neural networks from scratch, then in Keras. Learn: [3Blue1Brown neural networks](https://www.3blue1brown.com/topics/neural-networks), the micrograd lecture in [Karpathy's Zero to Hero](https://karpathy.ai/zero-to-hero.html), [TensorFlow tutorials](https://www.tensorflow.org/tutorials). Build: a small dense network on the W4 data.
- [ ] **W8 · Dec 21** — Break week (Christmas). Catch up or re-read anything that didn't land.
- [ ] **W9 · Dec 28** — **Project 1: credit card fraud detection.** Neural net vs. gradient boosting on a 0.17% fraud rate; report PR-AUC and the cost of each error type. Also read [Fed SR 11-7](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm) and write a one-page model card. This is the banking piece the course leaves out.

### Course 3: Generative AI for NLP (Weeks 10–15)

- [ ] **W10 · Jan 4** — How LLMs work; prompt engineering. Learn: Karpathy's "Let's build GPT" lecture, [Anthropic's prompt engineering tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial), [Hugging Face LLM course](https://huggingface.co/learn/llm-course) chapters 1–3. Build: support ticket categorization, prompt vs. a fine-tuned small classifier.
- [ ] **W11 · Jan 11** — Evaluating GenAI: test sets, LLM-as-judge, error analysis. Learn: [Hamel Husain on evals](https://hamel.dev/blog/posts/evals/), [DSPy](https://dspy.ai/) docs. Build: stock news sentiment with a 100-item labeled eval set, then let DSPy optimize the prompt and compare.
- [ ] **W12 · Jan 18** — Retrieval-augmented generation: embeddings, chunking, vector search. Learn: [Sentence Transformers](https://sbert.net/), [Chroma docs](https://docs.trychroma.com/), [LangChain docs](https://docs.langchain.com/) RAG tutorial. Build: a RAG assistant over public regulatory text (for example CFPB Regulation Z) instead of the course's clinical docs.
- [ ] **W13 · Jan 25** — Responsible AI and guardrails. Learn: [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) core, Llama Guard model card. Build: add input/output guardrails and refusal tests to the W12 assistant.
- [ ] **W14 · Feb 1** — Break week.
- [ ] **W15 · Feb 8** — **Project 2: regulatory policy assistant.** Finish W12–13 into one app with an eval harness: retrieval hit rate, answer faithfulness, refusal accuracy, cost per query.

### Course 4: Agentic AI for Automation (Weeks 16–19)

- [ ] **W16 · Feb 15** — Single-agent systems: tool use, the agent loop, when not to use an agent. Learn: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), [LangChain Academy](https://academy.langchain.com/) LangGraph intro. Build: reimbursement automation that extracts receipt fields and checks them against a written policy.
- [ ] **W17 · Feb 22** — Memory, MCP, structured outputs. Learn: [Model Context Protocol](https://modelcontextprotocol.io/) docs, [Hugging Face Agents Course](https://huggingface.co/learn/agents-course). Build: an MCP server that exposes the W16 policy check as a tool.
- [ ] **W18 · Mar 1** — Multi-agent systems and evaluating agents: tracing, trajectory evals, human-in-the-loop. Learn: LangGraph multi-agent and LangSmith docs. Build: supervisor plus two worker agents, with traces.
- [ ] **W19 · Mar 8** — **Project 3: helpdesk copilot.** Classify ticket, retrieve knowledge, draft a grounded reply, escalate when unsure. Report the escalation rate and a sample of 20 graded traces.

### Course 5: Deploying AI Solutions (Weeks 20–23)

- [ ] **W20 · Mar 15** — Deploying an ML model: FastAPI, Docker, a Streamlit front end. Learn: [Made With ML](https://madewithml.com/), [Docker get-started](https://docs.docker.com/get-started/), [Streamlit docs](https://docs.streamlit.io/). Build: containerize the Project 1 fraud model.
- [ ] **W21 · Mar 22** — Deploying GenAI on AWS: Lambda or a container behind API Gateway, Bedrock or an external API, logging, cost and latency budgets, drift monitoring. Build: put Project 2 behind an endpoint with Terraform, using your own AWS account.
- [ ] **W22 · Mar 29** — **Capstone, part 1.** Pick one problem, write a two-page design doc first: requirements, architecture, eval plan, risks.
- [ ] **W23 · Apr 5** — **Capstone, part 2.** Ship it: deployed app, eval report, model card, and a 5-minute recorded demo.

## Project portfolio

Every case study the course lists has a free public dataset or an equivalent; three are swapped for banking-relevant versions.

| Course case study | Week | Free data to use |
| --- | --- | --- |
| Ride-sharing demand analysis | W2 | [NYC TLC trip records](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) |
| Credit card eligibility insights | W3, W5 | [Credit Card Approval Prediction (Kaggle)](https://www.kaggle.com/datasets/rikdifos/credit-card-approval-prediction) |
| Insurance premium prediction | W4 | [Medical Cost Personal (Kaggle)](https://www.kaggle.com/datasets/mirichoi0218/insurance) |
| Shared bike demand prediction | W6 | [UCI Bike Sharing](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) |
| Predictive maintenance | W6 | [UCI AI4I 2020](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset) |
| Credit card fraud detection (Project 1) | W9 | [ULB Credit Card Fraud (Kaggle)](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) |
| Support ticket categorization | W10 | [Bitext customer support (Hugging Face)](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset) |
| Stock news sentiment | W11 | [Financial PhraseBank (Hugging Face)](https://huggingface.co/datasets/takala/financial_phrasebank) |
| Clinical decision support, swapped to a regulatory assistant (Project 2) | W12–15 | [Regulation Z, 12 CFR 1026 (eCFR)](https://www.ecfr.gov/current/title-12/chapter-X/part-1026) |
| Telecom policy assistant, folded into guardrails | W13 | Same Regulation Z corpus |
| Reimbursement automation | W16–17 | Your own receipts plus a one-page expense policy you write |
| AI helpdesk copilot (Project 3) | W19 | Bitext tickets plus a small knowledge base you generate |
| Retail order chatbot (optional extra) | Any | A synthetic orders table in SQLite |

Keep all of it on public or synthetic data. Nothing from work goes in this repo, which also makes it safe to show in an interview.

## Replacing what the fee buys

The hardest thing to replace is outside accountability; the content is the easy part.

| What the course gives | Self-study substitute |
| --- | --- |
| Weekly live mentor sessions | Saturday build block, plus a written review of each project: paste the notebook and write-up into Claude with a rubric (correctness, leakage, metric choice, what a reviewer would reject) |
| Program manager and deadlines | A Sunday scheduled check-in that asks which box got ticked; one break week as the only slack |
| Faculty masterclasses | Stanford CS229 lectures (free on YouTube) when you want more theory than ISLP gives |
| Peer cohort | Hugging Face and LangChain community forums; one study partner if you can find one |
| Texas McCombs certificate | A public repo with four finished projects, write-ups, and a deployed capstone; add an AWS ML certification later if a credential line on the resume matters |

For the Principal/Staff track, the write-ups and the capstone design doc are worth more than the certificate. Publishing two or three of them is the closest equivalent to the credential.

**Sources:** [Great Learning program page](https://www.mygreatlearning.com/pg-program-online-artificial-intelligence-machine-learning) · [Fee listing](https://www.techinterview.org/bootcamp_directory/p/great-learning-ai-ml/)
