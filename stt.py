"""
stt.py — Speech-to-Text
Непрерывное слушание микрофона с VAD и распознавание речи через Whisper API (Groq)
"""

import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API"))

SAMPLE_RATE = 16000       # Гц — стандарт для распознавания речи
CHANNELS = 1              # Моно
CHUNK_DURATION = 0.1      # Длина одного чанка в секундах (100 мс)
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)
SILENCE_THRESHOLD = 500   # Порог RMS: ниже — тишина, выше — речь
SILENCE_TIMEOUT = 1.5     # Секунд тишины для завершения записи
MAX_DURATION = 10         # Максимальная длина одной записи в секундах

# Варианты транскрипции wake word "Voicebot" через Whisper
WAKE_PHRASES = [
    "voicebot",
    "войсбот",
    "voice bot",
    "войс бот",
    "voiceбот",
]


def record_until_silence() -> str | None:
    """
    Слушает микрофон непрерывно.
    Начинает запись при обнаружении речи (RMS > SILENCE_THRESHOLD).
    Останавливается после SILENCE_TIMEOUT секунд тишины.
    Возвращает путь к WAV файлу или None если ничего не записано.
    """
    audio_chunks = []
    silent_chunks = 0
    speaking = False
    silence_chunks_limit = int(SILENCE_TIMEOUT / CHUNK_DURATION)
    max_chunks = int(MAX_DURATION / CHUNK_DURATION)

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=np.int16) as stream:
        while True:
            chunk, _ = stream.read(CHUNK_SIZE)
            rms = float(np.sqrt(np.mean(chunk.astype(np.float32) ** 2)))

            if rms > SILENCE_THRESHOLD:
                if not speaking:
                    print("🎤 Речь обнаружена...")
                    speaking = True
                silent_chunks = 0
                audio_chunks.append(chunk.copy())

            elif speaking:
                silent_chunks += 1
                audio_chunks.append(chunk.copy())
                if silent_chunks >= silence_chunks_limit:
                    break

            if speaking and len(audio_chunks) >= max_chunks:
                print("⏱ Достигнут лимит записи")
                break

    if not audio_chunks:
        return None

    audio = np.concatenate(audio_chunks)
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
    Непрерывно слушает микрофон до конца фразы, затем распознаёт речь.
    Возвращает распознанный текст.
    """
    while True:
        audio_path = record_until_silence()
        if audio_path is None:
            continue
        text = recognize_speech(audio_path)
        if text:
            print(f"📝 Вы сказали: {text}")
            return text


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
