from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = Path(os.getenv("POLICY_PATH", ROOT / "policies" / "sops.yaml"))
if not POLICY_PATH.is_absolute():
    POLICY_PATH = ROOT / POLICY_PATH

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "12"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
