from typing import Any,Dict
from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults
from graph.state import State

web_search_tool = TavilySearchResults(max_results=3)

def web_search(state: State) -> Dict[str, Any]:
    print("Web Searching...")
    question = state["question"]
    documents = state["documents"]

    docs = web_search_tool.invoke({"query": question})
    web_results = [
        Document(
            page_content=d["content"],
            metadata={"source": d["url"]}
        )
        for d in docs
    ]

    # if documents is not None (no need , extend is enough):
    documents.extend(web_results)
    return {"documents": documents, "question": question}