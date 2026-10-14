from __future__ import annotations
from typing import Protocol,runtime_checkable
from echo_engine.contracts import SignalEstimate, UserInput, InteractionState, ResponsePlan

@runtime_checkable
class PerceptionModule(Protocol):
    def estimate(self, user_input: UserInput, state: InteractionState) -> SignalEstimate: ...

@runtime_checkable
class PolicyModule(Protocol):
    def choose(self, estimate: SignalEstimate, state: InteractionState) -> ResponsePlan: ...

@runtime_checkable
class LLMAdapter(Protocol):
    def generate(self, plan: ResponsePlan, user_input: UserInput,state: InteractionState) -> str: ...    

@runtime_checkable
class StateStore(Protocol):
    def get(self, session_id: str) -> InteractionState: ...
    def put(self, session_id: str, state: InteractionState) -> None: ...  

class Fake:
    def choose(self, signals, state): ...

class GetOnly:
    def get(self, session_id): ...

class FullStore:
    def get(self, session_id): ...
    def put(self, state): ...

