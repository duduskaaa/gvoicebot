# GVoiceBot

A Python voice assistant with a PySide6 GUI. Recognizes speech via Groq Whisper, dispatches commands to skill classes, and responds with Microsoft Neural TTS.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Module Descriptions](#module-descriptions)
  - [main.py](#mainpy)
  - [assistant.py](#assistantpy)
  - [stt.py](#sttpy)
  - [tts.py](#ttspy)
  - [skills/](#skills)
  - [gui/](#gui)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Usage](#usage)
- [References](#references)

---

## Features

- Wake-word activation — say **"Voice"** to start listening
- Inline command syntax — say **"Voice, what time is it"** to skip the confirmation step
- Text input — type commands directly in the GUI without using a microphone
- Skills: time, date, weather, calculator, reminder, greeting
- OOP skill system — each skill is an independent class; adding a new one requires a single file and one line in `main.py`

---

## Architecture

```
Microphone
    │
    ▼
stt.py  ──  listen_for_wake_word()  ──►  wake word detected?
                                              │ yes
                                              ▼
                                         listen()  (or inline command)
                                              │
                                              ▼
                                    assistant.py :: Assistant.process()
                                              │
                                    ┌─────────┴──────────┐
                                    │  skill.can_handle() │
                                    │  skill.execute()    │
                                    └─────────┬──────────┘
                                              │
                                              ▼
                                         tts.py :: speak()
                                              │
                                              ▼
                                           Speaker
```

The GUI runs `AssistantThread` in a background `QThread` so the interface stays responsive during recording and TTS playback.

---

## Project Structure

```
gvoicebot/
├── main.py               # Entry point; instantiates Assistant with all skills
├── assistant.py          # Assistant class — dispatches text to skills
├── stt.py                # Speech-to-text: microphone recording + Groq Whisper
├── tts.py                # Text-to-speech: edge-tts + miniaudio playback
│
├── skills/
│   ├── base.py           # Abstract Skill base class
│   ├── greeting.py       # GreetingSkill
│   ├── time_skill.py     # TimeSkill, DateSkill
│   ├── weather.py        # WeatherSkill (OpenWeatherMap)
│   ├── calculator.py     # CalculatorSkill
│   └── reminder.py       # ReminderSkill (threading.Timer)
│
├── gui/
│   ├── app.py            # QApplication setup, stylesheet (Catppuccin Macchiato)
│   ├── main_window.py    # MainWindow — root layout, wires all widgets
│   ├── assistant_thread.py  # QThread wrapping the voice loop
│   ├── state.py          # AssistantState enum + badge/color metadata
│   ├── env_utils.py      # .env file load/save helpers
│   └── widgets/
│       ├── chat_widget.py      # QTextEdit displaying conversation
│       ├── status_widget.py    # State badge (WAKE / REC / THINKING / SPEAKING)
│       ├── sidebar.py          # Icon sidebar (settings, exit)
│       └── settings_dialog.py  # API key editor
│
├── requirements.txt
└── README.md
```

---

## Module Descriptions

### main.py

Entry point. Creates an `Assistant` instance with all registered skills and exposes `process_query(text) -> str` for both the voice thread and the text input.

```python
_assistant = Assistant([
    GreetingSkill(),
    TimeSkill(),
    DateSkill(),
    WeatherSkill(),
    CalculatorSkill(),
    ReminderSkill(),
])

def process_query(text: str) -> str:
    return _assistant.process(text)
```

To add a new skill: create a class in `skills/`, import it here, and append an instance to the list.

---

### assistant.py

`Assistant` iterates over its skill list and delegates to the first skill whose `can_handle()` returns `True`.

```python
class Assistant:
    def process(self, text: str) -> str:
        for skill in self._skills:
            if skill.can_handle(text):
                return skill.execute(text)
        return "I did not understand the request. Please try again."
```

---

### stt.py

Handles microphone capture and transcription.

| Constant | Value | Description |
|---|---|---|
| `WAKE_WORD` | `"voice"` | Trigger phrase |
| `WAKE_WORD_DURATION` | `3` s | Recording window for wake detection |
| `DURATION` | `5` s | Recording window for commands |

**`listen_for_wake_word() -> (bool, str)`**
Records `WAKE_WORD_DURATION` seconds, transcribes via Groq Whisper, and checks whether the wake word is present.
Returns `(True, inline_command)` if detected. `inline_command` is non-empty when the user says *"Voice, \<command\>"* in one utterance — the assistant then skips the second recording step.

**`listen() -> str`**
Records `DURATION` seconds and returns the transcribed text.

Recording uses the device's native sample rate (auto-detected via `sd.query_devices`) to avoid silence caused by PipeWire/PulseAudio sample-rate mismatches.

---

### tts.py

Synthesizes speech and plays it synchronously.

| Constant | Value |
|---|---|
| `VOICE` | `"en-US-JennyNeural"` |

**`speak(text)`**
1. Calls `edge_tts.Communicate(text, VOICE).save()` asynchronously via `asyncio.run()`
2. Decodes the MP3 with `miniaudio.decode_file()`
3. Plays the raw PCM samples through `sounddevice.play(..., blocking=True)`

No API key required — edge-tts uses the public Microsoft Neural TTS endpoint.

---

### skills/

#### Base class — `skills/base.py`

```python
class Skill(ABC):
    keywords: list[str] = []

    def can_handle(self, text: str) -> bool:
        return any(kw in text.lower() for kw in self.keywords)

    @abstractmethod
    def execute(self, text: str) -> str: ...
```

Override `keywords` and implement `execute()` to create a new skill.

---

#### GreetingSkill

**Triggers:** `hello`, `hi`, `good morning`, `good evening`, `hey`, `greetings`

Returns a fixed greeting string.

---

#### TimeSkill

**Triggers:** `time`, `what time`, `current time`, `clock`

Returns the current wall-clock time: *"It is 14:35."*

#### DateSkill

**Triggers:** `date`, `what day`, `today`, `what is today`

Returns the current date: *"Today is Friday, April 25, 2026."*

---

#### WeatherSkill

**Triggers:** `weather`, `temperature`, `outside`

Extracts a city name from the phrase *"weather in \<City\>"* using a regex. Falls back to `Almaty` if no city is found. Queries the OpenWeatherMap Current Weather API and returns temperature, description, and feels-like value.

Requires `OPENWEATHER_API` environment variable.

---

#### CalculatorSkill

**Triggers:** `calculate`, `compute`, `how much is`, `what is`, `equals`

Converts spoken operators to symbols before evaluation:

| Phrase | Operator |
|---|---|
| plus | `+` |
| minus | `-` |
| times | `*` |
| multiplied by | `*` |
| divided by | `/` |
| over | `/` |

Uses `eval()` on a character-whitelist-filtered string. Handles `ZeroDivisionError` explicitly.

---

#### ReminderSkill

**Triggers:** `remind me`, `set a reminder`, `reminder in`

Parses duration from phrases like *"remind me in 5 minutes to check the oven"*.
Schedules a `threading.Timer` that calls `tts.speak()` when the time elapses.

Supported units: `seconds`, `minutes`, `hours`.

---

### gui/

#### app.py

Sets up `QApplication`, applies the Catppuccin Macchiato stylesheet, loads `.env`, and shows `MainWindow`.

#### main_window.py

Root window layout:

```
┌──────┬────────────────────────────────┐
│      │  StatusWidget                  │
│      ├────────────────────────────────┤
│ Side │  ChatWidget (conversation log) │
│ bar  ├────────────────────────────────┤
│      │  [text input field]  [Send]    │
│      ├────────────────────────────────┤
│      │  [Activate]                    │
└──────┴────────────────────────────────┘
```

Text input runs `_TextWorker(QThread)` on submit so network-bound skills (weather) do not block the UI.

#### assistant_thread.py

`AssistantThread(QThread)` runs the voice loop:
1. Calls `listen_for_wake_word()`
2. If inline command present — skips to step 4
3. Speaks *"Yes?"* and calls `listen()`
4. Emits `message_added("user", text)`, calls `process_query()`, emits `message_added("bot", response)`, speaks the response

`activate()` bypasses wake-word detection for the next iteration (triggered by the **Activate** button).

#### state.py

Defines `AssistantState` enum and display metadata:

| State | Badge | Color |
|---|---|---|
| WAKE | WAKE | purple |
| COMMAND | REC | red |
| PROCESSING | THINKING | yellow |
| SPEAKING | SPEAKING | green |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API` | Yes | Groq API key for Whisper transcription |
| `OPENWEATHER_API` | For weather skill | OpenWeatherMap API key |

Keys can be set in a `.env` file at the project root or via the **Settings** dialog inside the app.

```
GROQ_API=gsk_...
OPENWEATHER_API=...
```

---

## Installation

Python 3.10+ required.

```bash
git clone <repo-url>
cd gvoicebot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Linux:** `sounddevice` requires PortAudio:
```bash
sudo apt install libportaudio2        # Debian/Ubuntu
sudo pacman -S portaudio              # Arch
```

---

## Usage

```bash
python main.py
```

### Voice activation

| Action | How |
|---|---|
| Wake word only | Say **"Voice"** → assistant says "Yes?" → say your command |
| Inline command | Say **"Voice, what time is it"** → answer immediately |
| Manual activate | Click the **Activate** button |

### Text input

Type any command in the text field and press **Enter** or **Send**.

### Example commands

```
Voice, what time is it
Voice, what is today
Voice, weather in London
Voice, what is 15 times 8
Voice, remind me in 10 minutes to take a break
hello
```

---

## References

1. Groq API — Whisper Speech Recognition: https://console.groq.com/docs/speech-text
2. rany2 — edge-tts Python library: https://github.com/rany2/edge-tts
3. OpenWeatherMap — Current Weather API: https://openweathermap.org/current
4. Radford A. et al. — Whisper: Robust Speech Recognition via Large-Scale Weak Supervision, OpenAI 2022: https://arxiv.org/abs/2212.04356
5. SoundDevice — Python bindings for PortAudio: https://python-sounddevice.readthedocs.io
6. miniaudio — Python bindings for miniaudio: https://github.com/irmen/pyminiaudio
7. PySide6 Documentation: https://doc.qt.io/qtforpython
