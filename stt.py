import re
import sounddevice as sd
import numpy as np
import wave
import os
from groq import Groq

SAMPLE_RATE = 44100
CHANNELS = 1
DURATION = 5
WAKE_WORD_DURATION = 3
WAKE_WORD = "voice"
SILENCE_THRESHOLD = 2000  # RMS below this is treated as silence


def _record(duration):
    print(f"🎤 Recording {duration} seconds...")
    device = sd.query_devices(kind="input")
    native_rate = int(device["default_samplerate"])
    audio = sd.rec(
        int(duration * native_rate),
        samplerate=native_rate,
        channels=CHANNELS,
        dtype=np.int16,
    )
    sd.wait()
    return audio, native_rate


def _is_silent(audio: np.ndarray) -> bool:
    rms = np.sqrt(np.mean(audio.astype(np.float32) ** 2))
    return rms < SILENCE_THRESHOLD


def _save_wav(audio: np.ndarray, rate: int) -> str:
    audio_path = "audio.wav"
    with wave.open(audio_path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(audio.tobytes())
    return audio_path


def _transcribe(audio_path: str) -> str:
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
    """Returns (detected: bool, inline_command: str).

    Inline command is non-empty when the user says 'Voice, <command>'
    in a single utterance, e.g. 'Voice, what time is it'.
    """
    audio, rate = _record(WAKE_WORD_DURATION)
    if _is_silent(audio):
        return False, ""

    text = _transcribe(_save_wav(audio, rate)).lower()
    if text:
        print(f"👂 Heard: {text}")

    if WAKE_WORD not in text:
        return False, ""

    # Strip the wake word (and optional punctuation/space) to get inline command
    after = re.sub(rf".*\b{WAKE_WORD}\b[,\s.!?]*", "", text).strip(".,!? ")
    return True, after
