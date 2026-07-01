from langchain.pydantic_v1 import BaseModel,Field
from typing import Literal

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

class RiskScorer(BaseModel):
    score: Literal["low", "medium", "high"] = Field(
        ...,
        description="risk score"
    )


llm = ChatOpenAI(temperature=0)
structured_llm = llm.with_structured_output(RiskScorer)

system_prompt = """
You are a financial risk assessment expert.
Based on the provided documents and question, assess the financial risk level.

- high: significant financial threats, instability, or critical vulnerabilities detected
- medium: moderate risks present but manageable, some concerns identified  
- low: minimal risk, stable financials, no major concerns detected

Analyze carefully and return only the risk score.
"""

scorer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Question: {question} \n\n Documents: {documents}")
    ]
)

risk_scorer_chain = scorer_prompt | structured_llm

