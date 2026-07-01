from langgraph.graph import StateGraph,END
from nodes import *
from nodes.route_question import route_question
from graph.state import State
from nodes.rag_search import rag_search
from nodes.risk_scorer import risk_scorer
from nodes.synthesize import synthesize
from nodes.web_search import web_search
from nodes.handle_failure import handle_failure
from typing import Dict
from chains.hallucination_grader import hallucination_grader
from dotenv import load_dotenv

load_dotenv()

graph = StateGraph(state_schema=State)

def grade_hallucination(state: State) -> str:
    question = state["question"]
    documents = state["documents"]
    generation = state["report"]
    retry_count = state["retry_count"]

    result = hallucination_grader.invoke({
        "question": question,
        "documents": documents,
        "report": generation
    })

    if result.binary_score:
        return "grounded"
    elif retry_count >= 3:
        return "failed"
    else:
        return "not grounded"



graph.set_conditional_entry_point(
    route_question,
    {"websearch": "web_search", "vectorstore": "rag_search"})

graph.add_node("web_search", web_search)
graph.add_node("rag_search", rag_search)
graph.add_node("synthesize", synthesize)
graph.add_node("risk_scorer", risk_scorer)
graph.add_node("handle_failure", handle_failure)


graph.add_edge("web_search", "synthesize")
graph.add_edge("rag_search", "synthesize")
graph.add_conditional_edges(
    "synthesize",
    grade_hallucination,
    {"grounded": "risk_scorer", "not grounded": "synthesize", "failed": "handle_failure"}
)
graph.add_edge("risk_scorer", END)
graph.add_edge("handle_failure", END)

app = graph.compile()

