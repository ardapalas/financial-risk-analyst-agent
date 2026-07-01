
from graph.state import State

def handle_failure(state: State):
    question = state["question"]

    fallback_report = (
        "Yeterli güvenilirlikte bir analiz üretilemedi. "
        "Mevcut kaynaklardan elde edilen bilgiler doğrulanamadı, "
        "bu nedenle güvenilir bir risk değerlendirmesi sunulamamaktadır."
    )

    return {"report": fallback_report, "risk_score": "unknown", "status": "failed"}