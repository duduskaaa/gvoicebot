import os
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent / ".env"


def load_env():
    if not ENV_PATH.exists():
        return
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


def save_env(updates: dict[str, str]):
    existing: dict[str, str] = {}
    if ENV_PATH.exists():
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    existing[key.strip()] = value.strip()
    existing.update(updates)
    with open(ENV_PATH, "w") as f:
        for key, value in existing.items():
            f.write(f"{key}={value}\n")
