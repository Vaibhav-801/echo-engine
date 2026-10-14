from echo_engine.components import KeywordPerception, RulePolicy, MockLLM, InMemoryStateStore
from echo_engine.contracts import InteractionState, UserInput, ResponsePlan, Strategy, Turn,EngineResponse
# from __future__ import annotations
import time

class EchoEngine:
    def __init__(self, perception,policy, llm, store):
        self.perception = perception
        self.policy = policy
        self.llm = llm
        self.store = store

    def respond(self, session_id, text) -> EngineResponse:
        start=time.perf_counter()
        user_input = UserInput(session_id, text)
        state = self.store.get(session_id)
        signals = self.perception.estimate(user_input, state)
        plan = self.policy.choose(signals, state)
        reply=self.llm.generate(plan, user_input, state)
        turn=Turn(
            text,
            signals,
            plan.strategy,
            reply,    
        )
        new_state = InteractionState(session_id, state.turns + (turn,))
        self.store.put(new_state)
        latency_ms=(time.perf_counter()-start)*1000
        return EngineResponse(
    session_id=session_id,
    text=reply,
    signals=signals,
    plan=plan,
    latency_ms=latency_ms,
    turn_index=state.turn_count,
)

engine = EchoEngine(KeywordPerception(), RulePolicy(), MockLLM(), InMemoryStateStore())
for msg in ["hello there", "I feel so sad and lonely", "I love this, so happy"]:
    r = engine.respond("s1", msg)
    print(r.turn_index, r.plan.strategy.value, "|", r.text)
print(engine.store.get("s1").turn_count)    