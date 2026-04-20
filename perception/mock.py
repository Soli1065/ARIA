import random
import time
from foundation.logger import get_logger

logger = get_logger("PERCEPTION")

def get_distance() -> float:
    """Ultrasonic — returns distance in cm."""
    value = round(random.uniform(15.0, 200.0), 1)
    logger.debug(f"Ultrasonic: {value}cm")
    return value

def get_sound_direction() -> dict:
    """Sound direction — returns angle and intensity."""
    angle = random.choice([0, 45, 90, 135, 180, 225, 270, 315])
    intensity = round(random.uniform(30.0, 90.0), 1)
    logger.debug(f"Sound: {intensity}dB at {angle}°")
    return {"angle": angle, "intensity": intensity}

def get_touch() -> bool:
    """Touch sensor — returns True if touched."""
    touched = random.random() < 0.2
    if touched:
        logger.debug("Touch: contact detected")
    return touched

def get_orientation() -> dict:
    """IMU — returns pitch, roll, yaw in degrees."""
    orientation = {
        "pitch": round(random.uniform(-10.0, 10.0), 2),
        "roll":  round(random.uniform(-5.0, 5.0), 2),
        "yaw":   round(random.uniform(0.0, 360.0), 2),
    }
    logger.debug(f"IMU: {orientation}")
    return orientation

def get_camera_frame() -> dict:
    """Camera — returns mock vision data."""
    objects = random.choice([
        [],
        [{"label": "person", "confidence": 0.91}],
        [{"label": "chair", "confidence": 0.78}],
        [{"label": "person", "confidence": 0.85},
         {"label": "cup",    "confidence": 0.62}],
    ])
    logger.debug(f"Camera: detected {len(objects)} object(s) — {objects}")
    return {"objects": objects, "timestamp": time.time()}

def get_speech_input() -> str:
    """Microphone — returns mock speech-to-text."""
    phrases = [
        "Hey ARIA, what do you see?",
        "ARIA, come here.",
        "How are you doing?",
        "ARIA, patrol the room.",
        "",  # silence
        "",  # silence more common
    ]
    text = random.choice(phrases)
    if text:
        logger.debug(f"STT: heard '{text}'")
    return text

def sense_all() -> dict:
    """Run all sensors and return combined perception snapshot."""
    logger.info("Perception snapshot taken")
    return {
        "distance":       get_distance(),
        "sound":          get_sound_direction(),
        "touch":          get_touch(),
        "orientation":    get_orientation(),
        "camera":         get_camera_frame(),
        "speech":         get_speech_input(),
    }
