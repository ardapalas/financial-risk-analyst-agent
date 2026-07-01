from chains.synthesis_chain import synthesis_chain
from graph.state import State


def synthesize(state: State):
    question = state["question"]
    documents = state["documents"]
    retry_count = state["retry_count"]

    retry_count = retry_count + 1

    result = synthesis_chain.invoke({
        "question": question,
        "documents": documents
    })

    return {"report": result, "retry_count": retry_count}

