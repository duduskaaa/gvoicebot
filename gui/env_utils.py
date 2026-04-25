import os
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent / ".env"


def _parse_env_line(line: str) -> tuple[str, str] | None:
    line = line.strip()
    if "=" not in line or line.startswith("#"):
        return None
    key, value = line.split("=", 1)
    return key.strip(), value.strip()


def load_env():
    if not ENV_PATH.exists():
        return
    with open(ENV_PATH) as f:
        for line in f:
            parsed = _parse_env_line(line)
            if parsed:
                os.environ.setdefault(*parsed)


def save_env(updates: dict[str, str]):
    existing: dict[str, str] = {}
    if ENV_PATH.exists():
        with open(ENV_PATH) as f:
            for line in f:
                parsed = _parse_env_line(line)
                if parsed:
                    existing[parsed[0]] = parsed[1]
    existing.update(updates)
    with open(ENV_PATH, "w") as f:
        for key, value in existing.items():
            f.write(f"{key}={value}\n")
