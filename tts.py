import asyncio
import os
import tempfile

import edge_tts
import miniaudio
import numpy as np
import sounddevice as sd

VOICE = "ru-RU-SvetlanaNeural"


def speak(text):
    print(f"🔊 Assistant: {text}")

    tmp_path = tempfile.mktemp(suffix=".mp3")
    asyncio.run(edge_tts.Communicate(text, VOICE).save(tmp_path))

    decoded = miniaudio.decode_file(tmp_path)
    os.remove(tmp_path)

    samples = np.frombuffer(bytes(decoded.samples), dtype=np.int16)
    if decoded.nchannels > 1:
        samples = samples.reshape(-1, decoded.nchannels)

    sd.play(samples, decoded.sample_rate, blocking=True)
