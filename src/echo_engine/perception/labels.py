"""Label vocabularies and the maps from each dataset's labels to ECHO's shared emotions."""
from __future__ import annotations

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


def to_echo(dataset: str, label: str) -> str:
    """Translate one dataset label into an ECHO emotion."""
    return MAPS[dataset][label]