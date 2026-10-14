from echo_engine.contracts import UNKNOWN, InteractionState, SignalEstimate, Turn, UserInput,ResponsePlan, Strategy
from echo_engine.interfaces import PerceptionModule, PolicyModule, StateStore
from typing import Protocol, runtime_checkable

class KeywordPerception:
    KEYWORDS ={
        "sad":("sad","lonely","depressed","cry"),
        "happy":("happy","joyful","excited","thrilled"),
        "angry":("angry","mad","furious","irate"),
        "anxious":("anxious","nervous","worried","stressed"),
    }
    def estimate(self, user_input, state):
        text=user_input.text.lower()
        hit={emo:sum(w in text for w in words) for emo,words in self.KEYWORDS.items()}
        best=max(hit,key=hit.get)
        if hit[best]==0:
            return SignalEstimate(
                emotion=UNKNOWN,
                emotion_confidence=0.0,
                intent="statement",
                intent_confidence=0.3,
                uncertain=True,
            )
        return SignalEstimate(
            emotion=best,
            emotion_confidence=min(0.9, 0.5 + 0.2 * hit[best]),
            intent="statement",
            intent_confidence=0.3,
            uncertain=False,
        )

class RulePolicy:
    NEGATIVE = ("sad", "anxious", "angry")

    def choose(self, signals, state) -> ResponsePlan:
        if signals.uncertain:
            return ResponsePlan(strategy=Strategy.CLARIFY, rationale="signals are uncertain")
        if signals.emotion in self.NEGATIVE and signals.emotion_confidence >= 0.6:
            return ResponsePlan(strategy=Strategy.EMPATHETIC, rationale=f"user seems {signals.emotion}")
        return ResponsePlan(strategy=Strategy.DIRECT, rationale="no strong emotion detected")

pol = RulePolicy()
perc = KeywordPerception()
s0 = InteractionState("s1")
for text in ["I feel so sad and lonely", "what time is it", "I love this, so happy"]:
    sig = perc.estimate(UserInput("s1", text), s0)
    print(text, "->", pol.choose(sig, s0))
print(isinstance(pol, PolicyModule))


class MockLLM:
    TEMPLATES = {
        Strategy.EMPATHETIC: "That sounds really hard. I'm here. Tell me more about it.",
        Strategy.CLARIFY: "Can you tell me a bit more about what you mean?",
        Strategy.DIRECT: "Got it: {text}",
        Strategy.CONCISE: "Okay.",
        Strategy.ABSTAIN: "I'm not able to help with that.",
    }

    def generate(self, plan, user_input, state) -> str:
        template = self.TEMPLATES[plan.strategy]
        return template.format(text=user_input.text)
@runtime_checkable
class LLMAdapter(Protocol):
    def generate(self, plan, user_input, state) -> str:
        ...

llm = MockLLM()
s0 = InteractionState("s1")
u = UserInput("s1", "I love this")

for strat in Strategy:
    print(
        strat.value,
        "->",
        llm.generate(ResponsePlan(strat, "test"), u, s0)
    )

class InMemoryStateStore:
    def __init__(self):
        self._sessions={}
    def get(self, session_id)->InteractionState:
        return self._sessions.get(session_id, InteractionState(session_id))
    def put(self, state)->None:
        self._sessions[state.session_id]=state    

store = InMemoryStateStore()
print(store.get("s1").turn_count)                      # 0, unknown session
t = Turn("hi", SignalEstimate(UNKNOWN, 0.0, "statement", 0.3, True), Strategy.CLARIFY, "tell me more")
store.put(InteractionState("s1", (t,)))
print(store.get("s1").turn_count)                     
print(store.get("other").turn_count)                  
print(isinstance(store, StateStore))                       