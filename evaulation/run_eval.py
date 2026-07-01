import json
from datasets import Dataset
from openai import AsyncOpenAI
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from dotenv import load_dotenv
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


load_dotenv()


evaluator_llm = LangchainLLMWrapper(langchain_llm=(ChatOpenAI(model="gpt-4.1-mini")))

evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))

with open("eval_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

dataset = Dataset.from_dict({
    "question": [d["question"] for d in data],
    "answer": [d["answer"] for d in data],
    "contexts": [d["contexts"] for d in data],
    "ground_truth": [d["ground_truth"] for d in data],
})

score = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    llm=evaluator_llm,
    embeddings=evaluator_embeddings
)

print(score)
df = score.to_pandas()
df.to_csv("eval_results.csv", index=False)