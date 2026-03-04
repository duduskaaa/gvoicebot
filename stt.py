"""
stt.py — Speech-to-Text
Запись микрофона (5 секунд) и распознавание речи через Whisper API (Groq)
"""

import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API"))

SAMPLE_RATE = 16000  # Гц — стандарт для распознавания речи
CHANNELS = 1         # Моно
DURATION = 5         # Длительность записи в секундах


def record_audio() -> str:
    """
    Записывает аудио с микрофона в течение DURATION секунд.
    Возвращает путь к временному WAV файлу.
    """
    print(f"🎤 Запись {DURATION} секунд...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                   channels=CHANNELS, dtype=np.int16)
    sd.wait()

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
    Записывает аудио и распознаёт речь.
    Возвращает распознанный текст.
    """
    audio_path = record_audio()
    text = recognize_speech(audio_path)
    if text:
        print(f"📝 Вы сказали: {text}")
    return text
