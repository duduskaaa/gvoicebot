import re

INTENTS = {
    "greeting": ["hello", "hi", "good morning", "good evening", "hey", "greetings"],
    "time": ["time", "what time", "current time", "clock"],
    "date": ["date", "what day", "today", "what is today"],
    "weather": ["weather", "temperature", "outside"],
    "calculator": ["calculate", "compute", "how much is", "what is", "equals"],
    "reminder": ["remind me", "set a reminder", "reminder in"],
}


def parse_intent(text):
    text = text.lower()

    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            if keyword in text:
                return intent

    return "unknown"


def extract_city(text):
    match = re.search(r"\bin\s+([A-Za-z]+)", text)
    if match:
        return match.group(1).capitalize()
    return "Almaty"
