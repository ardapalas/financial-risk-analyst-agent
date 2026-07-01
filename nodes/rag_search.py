from langchain_core.prompts import ChatPromptTemplate

from graph.ingestion import create_retriever
from graph.state import State
from graph.config import WEB_URLS
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)
retriever = create_retriever(WEB_URLS)

def rag_search(state: State):
    question = state["question"]
    documents = state["documents"]

    result = retriever.invoke(question)

    documents.extend(result)

    return {"documents": documents, "question": question}