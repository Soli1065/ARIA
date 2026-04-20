import logging
import colorlog
from datetime import datetime
from pathlib import Path
from config.settings import LOG_LEVEL

# ── Log file path ─────────────────────────────────────────
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"aria_{datetime.now().strftime('%Y%m%d')}.log"

# ── Colour map for terminal ───────────────────────────────
LOG_COLORS = {
    "DEBUG":    "cyan",
    "INFO":     "green",
    "WARNING":  "yellow",
    "ERROR":    "red",
    "CRITICAL": "bold_red",
}

def get_logger(layer: str) -> logging.Logger:
    """
    Returns a named logger for a given ARIA layer.
    Usage: logger = get_logger("AGENT_CORE")
    Output: [2026-04-19 14:32:01] [AGENT_CORE] [INFO] message
    """
    logger = logging.getLogger(layer)

    if logger.handlers:
        return logger  # already configured

    logger.setLevel(LOG_LEVEL)

    # ── Terminal handler (coloured) ───────────────────────
    terminal = colorlog.StreamHandler()
    terminal.setFormatter(colorlog.ColoredFormatter(
        fmt="%(log_color)s[%(asctime)s] [%(name)s] [%(levelname)s]%(reset)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors=LOG_COLORS,
    ))

    # ── File handler (plain text) ─────────────────────────
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(logging.Formatter(
        fmt="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    logger.addHandler(terminal)
    logger.addHandler(file_handler)
    return logger
