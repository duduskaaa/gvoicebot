#!/bin/bash
cd "$(dirname "$0")"

if [ -f ".venv/bin/python" ]; then
    exec .venv/bin/python main.py
elif [ -f "tts-venv/bin/python3" ]; then
    exec tts-venv/bin/python3 main.py
else
    exec python3 main.py
fi
