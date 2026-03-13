

INTENTS = {
    "greeting": ["hello", "hi", "good morning", "good evening", "hey", "greetings"],
    "time": ["time", "what time", "current time", "clock"],
    "date": ["date", "what day", "today", "what is today"],
    "weather": ["weather", "temperature", "outside"],
}


def parse_intent(text):
    text = text.lower()

    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            if keyword in text:
                return intent

    return "unknown"


def extract_city(text):
    words = text.split()
    if "in" in words:
        idx = words.index("in")
        if idx + 1 < len(words):
            return words[idx + 1].capitalize()
    return "Almaty"
