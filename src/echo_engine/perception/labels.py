"""Label vocabularies and the maps from each dataset's labels to ECHO's shared emotions."""
from __future__ import annotations
from dataclasses import dataclass

from sympy import true

ECHO_EMOTIONS = ("neutral", "happy", "sad", "angry", "anxious", "surprised", "disgusted")

MELD_TO_ECHO = {
    "neutral": "neutral",
    "joy": "happy",
    "sadness": "sad",
    "anger": "angry",
    "fear": "anxious",
    "surprise": "surprised",
    "disgust": "disgusted",
}

DD_EMOTION_TO_ECHO = {
    "no emotion": "neutral",
    "happiness": "happy",
    "sadness": "sad",
    "anger": "angry",
    "fear": "anxious",
    "surprise": "surprised",
    "disgust": "disgusted",
}

GOEMOTIONS_TO_ECHO = {
    "admiration": "happy",
    "amusement": "happy",
    "anger": "angry",
    "annoyance": "angry",
    "approval": None,
    "caring": None,
    "confusion": None,
    "curiosity": None,
    "desire": None,
    "disappointment": "sad",
    "disapproval": None,
    "disgust": "disgusted",
    "embarrassment": None,
    "excitement": "happy",
    "fear": "anxious",
    "gratitude": "happy",
    "grief": "sad",
    "joy": "happy",
    "love": "happy",
    "nervousness": "anxious",
    "optimism": "happy",
    "pride": "happy",
    "realization": None,
    "relief": "happy",
    "remorse": "sad",
    "sadness": "sad",
    "surprise": "surprised",
    "neutral": "neutral",
}

ED_TO_ECHO = {
    "surprised": "surprised",
    "excited": "happy",
    "annoyed": "angry",
    "proud": "happy",
    "angry": "angry",
    "sad": "sad",
    "grateful": "happy",
    "lonely": "sad",
    "impressed": "happy",
    "afraid": "anxious",
    "disgusted": "disgusted",
    "confident": None,
    "terrified": "anxious",
    "hopeful": "happy",
    "anxious": "anxious",
    "disappointed": "sad",
    "joyful": "happy",
    "prepared": None,
    "guilty": "sad",
    "furious": "angry",
    "nostalgic": None,
    "jealous": None,
    "anticipating": None,
    "embarrassed": None,
    "content": "happy",
    "devastated": "sad",
    "sentimental": None,
    "caring": None,
    "trusting": None,
    "ashamed": "sad",
    "apprehensive": "anxious",
    "faithful": None,
}

MAPS = {
    "meld": MELD_TO_ECHO,
    "dd_emotion": DD_EMOTION_TO_ECHO,
    "goemotions": GOEMOTIONS_TO_ECHO,
    "ed": ED_TO_ECHO,
}

@dataclass(frozen=True)
class Task:
    name: str
    kind: str
    classes: tuple


TASKS= {
    "meld": Task("meld", "single", tuple(sorted(MELD_TO_ECHO))),
    "goemotions": Task("goemotions", "multi", tuple(sorted(GOEMOTIONS_TO_ECHO))),
    "dd_emotion": Task("dd_emotion", "single", tuple(sorted(DD_EMOTION_TO_ECHO))),
    "ed": Task("ed", "single", tuple(sorted(ED_TO_ECHO))),
    "dd_act": Task("dd_act", "single", ("commissive", "directive", "inform", "question")),
    "echo": Task("echo", "single", tuple(ECHO_EMOTIONS)),
}

DATASET_TASKS={
    "goemotions": ["goemotions"],
    "meld": ["meld"],
    "ed": ["ed"],
    "dailydialog": ["dd_emotion", "dd_act"],
}

def echo_target(dataset: str, y: dict):
    """Return the shared ECHO emotion for one example, or None."""
    if dataset == "dailydialog":
        return to_echo("dd_emotion", y["dd_emotion"])
    if dataset == "goemotions":
        mapped = [to_echo("goemotions", name) for name in y["goemotions"]]
        mapped = [m for m in mapped if m is not None]
        if not mapped:
            return None
        for m in mapped:
            if m != "neutral":
                return m
        return "neutral"
    return to_echo(dataset, y[dataset])

def to_echo(dataset: str, label: str) -> str:
    """Translate one dataset label into an ECHO emotion."""
    return MAPS[dataset][label]