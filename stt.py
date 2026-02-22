"""
stt.py — Speech-to-Text
Запись с микрофона и распознавание речи через Whisper API (Groq)
"""

import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API"))

SAMPLE_RATE = 16000   # Гц — стандарт для распознавания речи
DURATION = 5          # Секунд записи
CHANNELS = 1          # Моно

# Варианты транскрипции wake word "GVoice" через Whisper
WAKE_PHRASES = [
    "gvoice",
    "g voice",
    "джи войс",
    "джейвойс",
    "джи-войс",
    "gвойс",
]


def extract_wake_command(text: str) -> tuple[bool, str]:
    """
    Проверяет наличие wake word в тексте.
    Возвращает (True, команда) если wake word найден, иначе (False, "").
    """
    lower = text.lower().strip()

    for phrase in WAKE_PHRASES:
        if phrase in lower:
            idx = lower.find(phrase)
            after = text[idx + len(phrase):].strip()
            after = after.lstrip(",.!? ")
            return True, after

    return False, ""


def record_audio(duration: int = DURATION) -> str:
    """
    Записывает аудио с микрофона.
    Возвращает путь к временному .wav файлу.
    """
    print(f"🎤 Говорите... ({duration} сек)")

    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=np.int16
    )
    sd.wait()  # Ждём окончания записи

    # Сохраняем во временный файл
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with wave.open(tmp.name, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit = 2 байта
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

    return tmp.name


def recognize_speech(audio_path: str) -> str:
    """
    Распознаёт речь из .wav файла через Whisper (Groq).
    Возвращает текст.
    """
    with open(audio_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3",
            language="ru",
            response_format="text"
        )

    os.unlink(audio_path)  # Удаляем временный файл
    return transcription.strip()


def listen() -> str:
    """
    Удобная функция: записывает и сразу распознаёт.
    Возвращает текст того, что сказал пользователь.
    """
    audio_path = record_audio()
    text = recognize_speech(audio_path)
    print(f"📝 Вы сказали: {text}")
    return text
