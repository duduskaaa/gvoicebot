import os
import re
import wave

import numpy as np
import sounddevice as sd #
from groq import Groq #

CHANNELS = 1
DURATION = 3
WAKE_WORD_DURATION = 3
WAKE_WORD = "voice"
SILENCE_THRESHOLD = 500


def _get_rate() -> int:
    return int(sd.query_devices(kind="input")["default_samplerate"])


def _record(duration: float) -> tuple[np.ndarray, int]:
    print(f"🎤 Recording {duration}s...")
    rate = _get_rate()
    audio = sd.rec(int(duration * rate), samplerate=rate, channels=CHANNELS, dtype=np.int16) #
    sd.wait()
    return audio, rate


def _is_silent(audio: np.ndarray) -> bool:
    rms = np.sqrt(np.mean(audio.astype(np.float32) ** 2))
    return rms < SILENCE_THRESHOLD


def _save_wav(audio: np.ndarray, rate: int) -> str: #
    audio_path = "audio.wav"
    with wave.open(audio_path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(audio.tobytes())
    return audio_path


def _transcribe(audio_path: str) -> str: #
    client = Groq(api_key=os.environ.get("GROQ_API"))
    with open(audio_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3",
            language="en",
            response_format="text",
        )
    os.remove(audio_path)
    return transcription.strip()


def listen() -> str:
    audio, rate = _record(DURATION)
    if _is_silent(audio):
        return ""
    text = _transcribe(_save_wav(audio, rate))
    if text:
        print(f"📝 You said: {text}")
    return text


def listen_for_wake_word():
    audio, rate = _record(WAKE_WORD_DURATION)
    if _is_silent(audio):
        return False, ""

    text = _transcribe(_save_wav(audio, rate)).lower()
    if text:
        print(f"👂 Heard: {text}")

    if WAKE_WORD not in text:
        return False, ""

    after = re.sub(rf".*\b{WAKE_WORD}\b[,\s.!?]*", "", text).strip(".,!? ")
    return True, after
