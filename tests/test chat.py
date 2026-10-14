"""Chat with ECHO in the terminal. Every turn is saved to data/turns.jsonl."""
from echo_engine.collector import JsonlCollector
from echo_engine.components import InMemoryStateStore, KeywordPerception, MockLLM, RulePolicy
from echo_engine.engine import EchoEngine


def main():
    engine = EchoEngine(KeywordPerception(), RulePolicy(), MockLLM(), InMemoryStateStore())
    collector = JsonlCollector("data/turns.jsonl")
    print("ECHO chat. Type 'quit' to stop.")

    while True:
        text = input("you> ").strip()
        if text.lower() == "quit":
            break
        if not text:
            continue
        response = engine.respond("me", text)
        collector.record(text, response)
        print(f"echo> {response.text}")
        print(f"      [{response.signals.emotion} {response.signals.emotion_confidence:.2f} -> {response.plan.strategy.value}]")


if __name__ == "__main__":
    main()