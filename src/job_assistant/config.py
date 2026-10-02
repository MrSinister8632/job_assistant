"""Application settings: load/save from data/settings.json."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

import sys

_root = Path(__file__).resolve().parents[2]
if getattr(sys, "frozen", False):  # running as packaged exe: keep data next to the exe
    _root = Path(sys.executable).resolve().parent
DATA_DIR = _root / "data"
SETTINGS_PATH = DATA_DIR / "settings.json"


@dataclass
class Settings:
    groq_api_key: str = ""
    gemini_api_key: str = ""
    adzuna_app_id: str = ""
    adzuna_app_key: str = ""
    jsearch_api_key: str = ""
    location_mode: str = "open_to_relocate"  # "specific" | "remote" | "open_to_relocate"
    location: str = ""
    resume_path: str = ""
    knowledge_path: str = ""
    resume_pages: int = 1
    keywords: str = ""

    def save(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        SETTINGS_PATH.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")

    @classmethod
    def load(cls) -> "Settings":
        if SETTINGS_PATH.exists():
            try:
                data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
                return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
            except (json.JSONDecodeError, TypeError):
                pass
        return cls()
