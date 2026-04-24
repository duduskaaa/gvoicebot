import sounddevice as sd
import numpy as np
import wave
import os
from groq import Groq

SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 5
WAKE_WORD_DURATION = 3
WAKE_WORD = "voicebot"


def _record(duration):
    print(f"🎤 Recording {duration} seconds...")
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=np.int16,
    )
    sd.wait()

    audio_path = "audio.wav"
    with wave.open(audio_path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

    return audio_path


def _transcribe(audio_path):
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


def listen():
    audio_path = _record(DURATION)
    text = _transcribe(audio_path)
    if text:
        print(f"📝 You said: {text}")
    return text


def listen_for_wake_word():
    audio_path = _record(WAKE_WORD_DURATION)
    text = _transcribe(audio_path).lower()
    if text:
        print(f"👂 Heard: {text}")
    return WAKE_WORD in text
