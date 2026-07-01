# Financial Risk Analyst Agent

A multi-step financial risk analysis agent built with **LangGraph**, combining Retrieval-Augmented Generation (RAG) and real-time web search to answer financial risk questions. The agent automatically routes queries to the appropriate data source, detects hallucinations in generated answers, and retries or gracefully falls back when confidence is low — all monitored through **LangSmith** and evaluated with **RAGAS**.

## Overview

Financial risk assessment requires both stable domain knowledge and up-to-date market information. This project addresses that by combining two retrieval strategies within a single LangGraph workflow:

- **RAG search** over a persistent vector store (ChromaDB) for grounded, domain-specific knowledge
- **Web search** (via Tavily) for time-sensitive queries, such as recent news or current events affecting a stock or sector

A routing layer decides which source to use per query, and a hallucination-grading step verifies that the final answer is actually supported by the retrieved context before it's returned.

## Architecture

```
                     ┌─────────────────┐
                     │  route_question │
                     └────────┬────────┘
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          ┌─────────────┐           ┌─────────────┐
          │  rag_search  │           │ web_search  │
          └──────┬───────┘           └──────┬──────┘
                 └────────────┬─────────────┘
                               ▼
                        ┌─────────────┐
                        │  synthesize │
                        └──────┬──────┘
                               ▼
                     ┌───────────────────┐
                     │ hallucination_grader│
                     └─────────┬──────────┘
                        pass  │  fail (retry ≤ 3)
                    ┌─────────┴─────────┐
                    ▼                   ▼
             ┌─────────────┐    ┌────────────────┐
             │ risk_scorer │    │ handle_failure │
             └─────────────┘    └────────────────┘
```

**Routing logic:** Time-sensitive queries (e.g. containing references to "today," recent news, or current events) are routed to web search; general financial risk questions are routed to the RAG pipeline over the vector store.

**Retry & fallback:** If the hallucination grader determines that a generated answer isn't sufficiently grounded in the retrieved context, the graph retries generation up to 3 times. If all retries fail, the agent returns a transparent fallback response rather than presenting an unverified answer as fact.

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | LangGraph |
| RAG / Retrieval | LangChain, ChromaDB |
| Web Search | Tavily API |
| LLM | OpenAI (GPT-4o-mini) |
| Observability | LangSmith |
| Evaluation | RAGAS (faithfulness, answer relevancy, context precision, context recall) |
| Language | Python |

## Project Structure

```
Financial-Risk-Analyst-Agent/
├── chains/
│   ├── router.py               # Query routing logic (RAG vs. web search)
│   ├── synthesis_chain.py      # Final answer generation
│   ├── hallucination_grader.py # Groundedness check on generated answers
│   └── risk_scorer.py          # Risk scoring chain
├── nodes/
│   ├── route_question.py
│   ├── rag_search.py
│   ├── web_search.py
│   ├── synthesize.py
│   ├── risk_scorer.py
│   └── handle_failure.py       # Fallback node after failed retries
├── graph/
│   ├── graph.py                # LangGraph graph definition
│   ├── state.py                # Shared state schema
│   ├── ingestion.py            # Vector store ingestion pipeline
│   └── config.py
├── evaluation/
│   ├── generate_results.py     # Generates model outputs for eval questions
│   ├── run_eval.py             # Runs RAGAS evaluation
│   ├── eval_questions.py
│   └── eval_data.json
├── main.py
└── requirements.txt
```

## Evaluation

The agent's output quality is evaluated using [RAGAS](https://docs.ragas.io/), an open-source framework for assessing RAG pipelines. Four metrics are tracked:

- **Faithfulness** — how well the generated answer is grounded in the retrieved context
- **Answer Relevancy** — how directly the answer addresses the question
- **Context Precision** — how much of the retrieved context is actually relevant
- **Context Recall** — how much of the necessary information was successfully retrieved

Because RAG evaluation and the LangGraph runtime have conflicting dependency requirements, evaluation runs in a separate virtual environment (`.venv-eval`) from the main agent (`.venv`).

## Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key
- Tavily API key

### Installation

```bash
git clone https://github.com/ardapalas/financial-risk-analyst-agent.git
cd financial-risk-analyst-agent

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
LANGCHAIN_API_KEY=your_langsmith_key   # optional, for observability
```

### Running the agent

```bash
python main.py
```

### Running the evaluation

```bash
python -m venv .venv-eval
source .venv-eval/bin/activate
pip install -r evaluation/requirements-eval.txt

cd evaluation
python generate_results.py   # generates eval_data.json using the main .venv
python run_eval.py           # scores the results with RAGAS
```

## Key Design Decisions

- **Separate virtual environments for evaluation:** RAGAS's dependency tree conflicts with LangGraph's, so evaluation is decoupled into its own environment to avoid version resolution issues.
- **Query-aware routing:** Rather than always retrieving from the vector store, the agent inspects the query for time-sensitivity signals and dynamically chooses between RAG and live web search.
- **Fail-safe generation:** A hallucination grader with bounded retries ensures the agent never silently returns an ungrounded answer — after 3 failed attempts, it explicitly reports that a reliable assessment couldn't be produced.

## Author

**Arda Palas**
[GitHub](https://github.com/ardapalas) · [LinkedIn](https://linkedin.com/in/ardapalas)
