import os
from dotenv import load_dotenv

load_dotenv()

# ── Environment ───────────────────────────────────────────
ARIA_ENV = os.getenv("ARIA_ENV", "development")
USE_MOCK_HARDWARE = os.getenv("ARIA_USE_MOCK_HARDWARE", "true").lower() == "true"

# ── Logging ───────────────────────────────────────────────
LOG_LEVEL = os.getenv("ARIA_LOG_LEVEL", "DEBUG")

# ── LLM ───────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")

# ── Validation ────────────────────────────────────────────
def validate():
    issues = []
    if not ANTHROPIC_API_KEY:
        issues.append("ANTHROPIC_API_KEY is not set in .env")
    if issues:
        for issue in issues:
            print(f"[CONFIG] WARNING: {issue}")
    return len(issues) == 0
