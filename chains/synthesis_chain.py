from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(temperature=0)

system_prompt = """
U are a financial risk analyzer.
Answer the question by reading the documens.
Your answer will be short and professional.
Documents: {documents}
"""

synthesizer_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{question}")
])

synthesis_chain = synthesizer_prompt | llm | StrOutputParser()