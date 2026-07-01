from graph.graph import app
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    result = app.invoke({
        "question":"what is the financial risk of investing in Tesla today?",
        "documents": [],
        "risk_score": "",
        "report":"",
        "retry_count":0
    })

    print(result["risk_score"])
    print(result["report"])