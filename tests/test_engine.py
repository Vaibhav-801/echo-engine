from echo_engine.components import InMemoryStateStore, KeywordPerception, MockLLM, RulePolicy
from echo_engine.contracts import Strategy
from echo_engine.engine import EchoEngine


def make_engine():
    return EchoEngine(KeywordPerception(), RulePolicy(), MockLLM(), InMemoryStateStore())

def test_sad_message_gets_empathetic_strategy():
    r = make_engine().respond("s1", "I feel so sad and lonely")
    assert r.plan.strategy == Strategy.EMPATHETIC


def test_unclear_message_asks_to_clarify():
    r = make_engine().respond("s1", "what time is it")
    assert r.plan.strategy == Strategy.CLARIFY
    assert r.signals.uncertain is True


def test_engine_remembers_turns_per_session():
    engine = make_engine()
    engine.respond("s1", "hello")
    engine.respond("s1", "I feel so sad and lonely")
    engine.respond("s2", "hello")
    assert engine.store.get("s1").turn_count == 2
    assert engine.store.get("s2").turn_count == 1

import pytest


def test_empty_message_is_rejected():
    with pytest.raises(ValueError):
        make_engine().respond("s1", "")    