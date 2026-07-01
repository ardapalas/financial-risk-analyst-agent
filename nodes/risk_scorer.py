from chains.risk_scorer import risk_scorer_chain
from graph.state import State


def risk_scorer(state: State):
    question = state["question"]
    documents = state["documents"]

    result = risk_scorer_chain.invoke({
        "question": question,
        "documents": documents
    })

    return {"risk_score": result.score}