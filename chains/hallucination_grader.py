from langchain.pydantic_v1 import BaseModel,Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class GradeHallucination(BaseModel):
    binary_score: bool = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )


llm = ChatOpenAI(temperature=0)
structured_llm = llm.with_structured_output(GradeHallucination)

system_prompt = """
You are a grader assessing whether an LLM generation is grounded in supported by a set of retrieved facts.
Give a binary score 'yes' or 'no'. 'yes' means the answer is grounded in the facts.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Question : {question} Documents : {documents} LLM Generation : {report}")
])

hallucination_grader = prompt | structured_llm
