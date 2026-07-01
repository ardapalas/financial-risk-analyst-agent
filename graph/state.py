from typing import TypedDict,List, Annotated, Sequence
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
import operator


class State(TypedDict):

    # originals
    question: str
    documents: List[Document]
    risk_score: str    # low-medium-high
    report: str
    retry_count: int
    status: str   # failed or success



