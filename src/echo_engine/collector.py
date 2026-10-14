from pathlib import Path
from echo_engine.components import KeywordPerception, RulePolicy, MockLLM, InMemoryStateStore,Tune
from echo_engine.engine import EchoEngine
from datetime import datetime,timezone
import json

class JsonlCollector:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, user_text,response)->None:
        row = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "session_id": response.session_id,
            "user_text": user_text,
            "emotion": response.signals.emotion,
            "emotion_confidence": response.signals.emotion_confidence,
            "strategy": response.plan.strategy.value,
            "reply": response.text,
            "label": None,
        }
        with self.file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

col = JsonlCollector("/tmp/echo_test/turns.jsonl")
engine = EchoEngine(KeywordPerception(), RulePolicy(), MockLLM(), InMemoryStateStore())
for msg in ["hello there", "I feel so sad and lonely"]:
    col.record(msg, engine.respond("s1", msg))

print(Path("/tmp/echo_test/turns.jsonl").read_text())