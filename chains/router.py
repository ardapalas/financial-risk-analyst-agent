from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.pydantic_v1 import BaseModel,Field
from typing import Literal
from dotenv import load_dotenv
from graph.state import State

load_dotenv()


class RouteQuery(BaseModel):
    datasources: Literal["vectorstore", "websearch"] = Field(
        ...,
        description="Given a user question choose to route it to web search or a vectorstore."
    )


llm = ChatOpenAI(temperature=0)
structured_llm_router = llm.with_structured_output(RouteQuery)

system_prompt = """
You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains financial documents such as annual reports, 
risk policies, and company financials. Use the vectorstore for questions 
about specific company documents. Use web search for current news, 
stock prices, or recent events.
IMPORTANT: If the question contains time-sensitive words such as 
"today", "now", "current", "this week", or "latest", ALWAYS choose 
websearch regardless of the topic, since the vectorstore only 
contains static historical documents.
"""

route_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])

question_router = route_prompt | structured_llm_router
