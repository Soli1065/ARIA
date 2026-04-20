import time
from foundation.logger import get_logger

logger = get_logger("EXPRESSION")

def speak(text: str):
    """TTS — logs what ARIA would say."""
    logger.info(f"SPEAK: \"{text}\"")

def move(action: str, **kwargs):
    """Servo movement — logs the action."""
    params = f" {kwargs}" if kwargs else ""
    logger.info(f"MOVE: {action}{params}")

def set_led(emotion: str, color: tuple = None):
    """LED — logs the emotional state display."""
    color_str = f" → RGB{color}" if color else ""
    logger.info(f"LED: {emotion}{color_str}")

def express(emotion: str):
    """Combined expression — movement + LED for an emotion."""
    expressions = {
        "happy":     ("wag_tail",   (0, 255, 0)),
        "curious":   ("tilt_head",  (0, 150, 255)),
        "alert":     ("stand_tall", (255, 165, 0)),
        "confused":  ("head_shake", (255, 0, 255)),
        "idle":      ("sit",        (50, 50, 50)),
    }
    action, color = expressions.get(emotion, ("idle", (50, 50, 50)))
    move(action)
    set_led(emotion, color)
    logger.info(f"EXPRESSION: {emotion}")

def stop():
    """Stop all movement."""
    logger.info("MOVE: stop — all servos halted")
