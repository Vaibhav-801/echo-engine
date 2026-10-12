from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

UNKNOWN="unknown"

class Strategy(str,Enum):
    """The strategy to use for the contract."""
    DIRECT= "direct"
    EMPATHETIC = "empathetic"
    CLARIFY="clarify"
    CONCISE="concise"
    ABSTAIN="abstain"

@dataclass(frozen=True)
class UserInput:
    session_id: str
    text: str

    def __post_init__(self):
        if not self.session_id:
            raise ValueError("session_id is required")
        if not self.text:
            raise ValueError("text is required")

@dataclass(frozen=True)
class SignalEstimate:
    emotion: str = UNKNOWN               
    emotion_confidence: float = 0.0
    intent: str = UNKNOWN                
    intent_confidence: float = 0.0       
    uncertain: bool = True

    def __post_init__(self) -> None:
        for name in ("emotion_confidence", "intent_confidence"):   # CHANGED: typo fixed
            value = getattr(self, name)
            if not (0.0 <= value <= 1.0):
                raise ValueError(f"{name} must be between 0.0 and 1.0, got {value}")        

@dataclass(frozen=True)
class ResponsePlan:
    strategy: Strategy
    rationale: str

@dataclass(frozen=True)
class Turn:
    user_text: str
    signals: SignalEstimate
    strategy: Strategy
    response_text: str

@dataclass(frozen=True)
class InteractionState:
    session_id: str
    turns: tuple[Turn, ...] = ()

    @property
    def turn_count(self) -> int:
        return len(self.turns)    

@dataclass(frozen=True)
class EngineResponse:
    session_id: str
    text: str
    signals: SignalEstimate
    plan: ResponsePlan
    latency_ms: float
    turn_index: int

SignalEstimate(intent_confidence=0.5)
SignalEstimate(emotion_confidence=1)

# print(UserInput("s1", "hello"))
# t = Turn("hi", SignalEstimate(), Strategy.CLARIFY, "tell me more")
# print(t)
# print(InteractionState("s1").turn_count)
# print(InteractionState("s1", (t,)).turn_count)