# Presentation Guide

---

## Slide 1 — Project Title

**Title:** GVoiceBot

**Subtitle:** Python Voice Assistant with GUI

**Also include:**
- Your name
- Course name
- Year

---

## Slide 2 — Project Goal

**One sentence goal:**
> Develop a desktop voice assistant in Python that accepts voice and text commands, processes them through a modular skill system, and responds with synthesized speech.

**3 bullet points — what the project solves:**
- Hands-free interaction via wake word activation
- Extensible command handling — each skill is an independent class
- Persistent conversation history stored in a local database

---

## Slide 3 — Technologies

**Table with two columns: Component / Technology**

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| GUI | PySide6 (Qt6) |
| Speech Recognition | Groq API — Whisper large-v3 |
| Text-to-Speech | edge-tts — Microsoft Neural TTS |
| Audio I/O | sounddevice, miniaudio |
| Weather | OpenWeatherMap API |
| Database | SQLite |

---

## Slide 4 — Architecture

**Title:** How it works

**Show the flow diagram — draw arrows between these blocks:**

```
Microphone → stt.py → assistant.py → skill.execute() → tts.py → Speaker
                                ↕
                              db.py
                                ↕
                           GUI (PySide6)
```

**Below the diagram — 3 bullet points:**
- `stt.py` records audio and transcribes via Groq Whisper
- `assistant.py` finds the matching skill and returns `(voice, display)`
- `tts.py` synthesizes and plays the response; `db.py` saves the message

---

## Slide 5 — Interface

**Title:** Interface

**Insert 2–3 screenshots from the `assets/` folder:**
- Main window with the chat area — `screenshot_main.png`
- Status bar states (WAKE / REC / THINKING / SPEAKING) — `screenshot_wake.png` and `screenshot_rec.png`
- Settings dialog — `screenshot_settings.png`

**One line caption under each screenshot describing what is shown.**

---

## Slide 6 — Key Features

**Title:** Features

**6 bullet points — one per skill / capability:**
- Wake word activation — say **"Voice"** to start
- Inline commands — say **"Voice, what time is it"** to skip confirmation
- Time & date — returns current time and date in English
- Weather — fetches live data from OpenWeatherMap by city name
- Calculator — evaluates spoken math expressions
- Reminders — schedules a spoken reminder after a given time
- Chat history — show, filter by today, or clear via voice or text command
- Text input — full functionality without a microphone
