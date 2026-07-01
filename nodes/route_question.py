from graph.state import State
from chains.router import question_router


def route_question(state: State) -> str:
    question = state["question"]
    result = question_router.invoke({"question": question})
    return result.datasources

