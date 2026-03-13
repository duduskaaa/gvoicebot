import asyncio
import time
import os
import edge_tts
import pygame


VOICE = "ru-RU-SvetlanaNeural"


def speak(text):
    print(f"🔊 Assistant: {text}")

    tmp_path = "output.mp3"

    communicate = edge_tts.Communicate(text, VOICE)
    asyncio.run(communicate.save(tmp_path))

    pygame.mixer.init()
    pygame.mixer.music.load(tmp_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.quit()
    os.remove(tmp_path)
