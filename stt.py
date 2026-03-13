import sounddevice as sd
import numpy as np
import wave
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API"))

SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 5


def record_audio():
    print(f"🎤 Recording {DURATION} seconds...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                   channels=CHANNELS, dtype=np.int16)
    sd.wait()

    audio_path = "audio.wav"
    with wave.open(audio_path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

    return audio_path


def recognize_speech(audio_path):
    with open(audio_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3",
            language="ru",
            response_format="text"
        )

    os.remove(audio_path)
    return transcription.strip()


def listen():
    audio_path = record_audio()
    text = recognize_speech(audio_path)
    if text:
        print(f"📝 You said: {text}")
    return text
