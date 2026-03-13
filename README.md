# Table of Contents

- [1. Introduction](#1-introduction)
- [2. System Architecture](#2-system-architecture)
- [3. Module Descriptions](#3-module-descriptions)
  - [3.1. main.py - Main Loop](#31-mainpy---main-loop)
  - [3.2. stt.py - Speech Recognition](#32-sttpy---speech-recognition)
  - [3.3. tts.py - Speech Synthesis](#33-ttspy---speech-synthesis)
  - [3.4. parser.py - Intent Classification](#34-parserpy---intent-classification)
  - [3.5. skills/ - Assistant Skills](#35-skills---assistant-skills)
- [4. Environment Variables](#4-environment-variables)
- [5. Installation and Launch](#5-installation-and-launch)
- [6. References](#6-references)

---

## 1. Introduction

GVoiceBot is a voice assistant written in Python, designed for natural language voice control. The system captures voice commands from the user, performs speech recognition, classifies the intent, and returns a corresponding spoken response.

The project targets Russian-speaking users and supports commands for querying the current time, date, weather, and greeting interactions. The architecture follows a separation-of-concerns principle: each module has a single well-defined responsibility.

The activation keyword (wake word) is "Voicebot". The system waits for the wake word before each command, which prevents false activations in background listening mode.

---

## 2. System Architecture

The system is composed of the following layers:

- **Input layer (STT):** Microphone recording -> speech recognition via the Whisper API (Groq).
- **Processing layer (Parser):** Text classification by keywords -> intent determination.
- **Skills layer:** Business logic for each intent: time, date, weather.
- **Output layer (TTS):** Speech synthesis via edge-tts (Microsoft Neural Voices) -> playback via pygame.

Data flow:

```
Microphone -> [STT] -> Text -> [Parser] -> Intent -> [Skill] -> Response -> [TTS] -> Speaker
```

---

## 3. Module Descriptions

### 3.1. main.py - Main Loop

`main.py` implements the main control loop of the assistant. The `main()` function starts the assistant, plays a greeting phrase, and enters an infinite command-processing loop.

The `process_query(text)` function receives the recognized text, calls `parse_intent()` to determine the intent, and dispatches execution to the corresponding skill. If the intent is unknown, it returns the phrase "I did not understand the request. Please try again."

Supported intents:

- `greeting` - greet the user
- `time` - query the current time
- `date` - query the current date
- `weather` - query the weather with an optional city

### 3.2. stt.py - Speech Recognition

The `stt.py` module is responsible for capturing audio from the microphone and transcribing it to text. Recording is performed using the sounddevice library at a sample rate of 16,000 Hz (the standard for ASR systems), in mono mode.

`record_audio()` records a fixed 5-second segment and saves it as a 16-bit WAV file in the system temp directory. `recognize_speech()` sends the file to the Groq Whisper API (model: whisper-large-v3, language: ru) and returns the transcribed text. The temporary file is deleted after successful recognition.

`listen()` combines recording and recognition into a single call and is used in the main loop.

### 3.3. tts.py - Speech Synthesis

The `tts.py` module synthesizes speech from text and plays it through the device audio output. Synthesis is performed via the edge-tts library, which uses Microsoft Neural TTS and does not require an API key.

Default voice: `ru-RU-SvetlanaNeural` (Russian female). An alternative is `ru-RU-DmitryNeural` (Russian male).

`speak(text)` saves the synthesized MP3 to a temporary file, loads it via `pygame.mixer`, and plays it synchronously — the function blocks until playback finishes. The temporary file is deleted afterwards.

Because `edge_tts.Communicate.save()` is a coroutine (`async def`), `asyncio.run()` is used to call it from synchronous code.

### 3.4. parser.py - Intent Classification

`parser.py` implements rule-based text classification. The `INTENTS` dictionary maps each intent name to a list of trigger keywords. `parse_intent(text)` lowercases the input and checks for substring matches.

Keywords by intent:

- `greeting`: hello, hi, good morning, good evening, hey
- `time`: time, what time, what is the time, clock
- `date`: date, what day, today, what is today
- `weather`: weather, temperature, outside

`extract_city(text)` extracts a city name from phrases such as "weather in Almaty" using a regular expression. If no match is found, the default city Almaty is returned.

### 3.5. skills/ - Assistant Skills

The `skills/` directory contains the implementation of each skill. At the current stage, skills are implemented as stubs.

- `time_skill.py`: `get_time()` returns the current time; `get_date()` returns the current date. In the final version, the `datetime` module is used.
- `weather.py`: `get_weather(city)` returns weather data. A stub dictionary covers Almaty and Astana. In the final version it queries the OpenWeatherMap API.

---

## 4. Environment Variables

The following environment variable must be set for the assistant to work:

- `GROQ_API`: API key for the Groq service to access the Whisper model. Obtained at console.groq.com after registration. Used in `stt.py` when initializing the Groq client.

Export the variable before running the assistant:

```bash
export GROQ_API="your_groq_key"
```

---

## 5. Installation and Launch

Requirements: Python 3.10 or higher.

Install dependencies:

```bash
pip install -r requirements.txt
```

Project dependencies (`requirements.txt`):

- groq
- edge-tts
- pygame
- sounddevice
- numpy
- requests

Launch:

```bash
python main.py
```

After launch, the assistant plays a greeting and enters listening mode. To activate a command, say the wake word "Voicebot" followed by your command. To stop the assistant, press `Ctrl+C`.

---

## 6. References

1. Groq API Documentation. Whisper Speech Recognition – https://console.groq.com/docs/speech-text.
2. rany2. edge-tts - Python library for Microsoft Edge TTS – https://github.com/rany2/edge-tts.
3. Radford A. et al. Whisper: Robust Speech Recognition via Large-Scale Weak Supervision. OpenAI, 2022 – https://arxiv.org/abs/2212.04356.
4. Pygame Documentation. pygame.mixer - Sound and Music – https://www.pygame.org/docs/ref/mixer.html.
5. SoundDevice Documentation. Python bindings for PortAudio – https://python-sounddevice.readthedocs.io.
6. OpenWeatherMap API. Current Weather Data – https://openweathermap.org/current.
7. Python Software Foundation. asyncio - Asynchronous I/O. Python 3 Documentation – https://docs.python.org/3/library/asyncio.html.
8. Lutz M. Learning Python. 5th ed. O'Reilly Media, 2013. 1540 p.
