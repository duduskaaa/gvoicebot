"""
tts.py — Text-to-Speech
Синтез речи через edge-tts (бесплатно, хороший русский голос)
"""

import asyncio
import tempfile
import os
import edge_tts
import pygame


VOICE = "ru-RU-SvetlanaNeural"  # Женский русский голос
# Альтернативы: "ru-RU-DmitryNeural" — мужской


def speak(text: str):
    """
    Озвучивает текст через edge-tts.
    Блокирует выполнение до окончания воспроизведения.
    """
    print(f"🔊 Ассистент: {text}")
    asyncio.run(_synthesize_and_play(text))


async def _synthesize_and_play(text: str):
    """
    Генерирует аудио и воспроизводит его.
    """
    # Сохраняем в временный mp3
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp_path = tmp.name
    tmp.close()

    # Синтез через edge-tts
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(tmp_path)

    # Воспроизведение через pygame
    pygame.mixer.init()
    pygame.mixer.music.load(tmp_path)
    pygame.mixer.music.play()

    # Ждём окончания
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.quit()
    os.unlink(tmp_path)  # Удаляем временный файл
