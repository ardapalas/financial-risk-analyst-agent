from dotenv import load_dotenv
load_dotenv()

import sys, os, json
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from graph.graph import app
from eval_questions import eval_questions

results = []

for item in eval_questions:
    question = item["question"]
    print(f"Çalıştırılıyor: {question}")

    state = app.invoke({
        "question": question,
        "documents": [],
        "retry_count": 0
    })

    results.append({
        "question": question,
        "answer": state["report"],
        "contexts": [doc.page_content for doc in state["documents"]],
        "ground_truth": item["ground_truth"]
    })

with open("eval_data.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("eval_data.json kaydedildi.")