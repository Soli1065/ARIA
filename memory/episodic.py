import json
from datetime import datetime
from pathlib import Path
from foundation.logger import get_logger

logger = get_logger("MEMORY")

EPISODIC_FILE = Path(__file__).parent.parent / "logs" / "episodic.jsonl"

class EpisodicMemory:
    """
    Long-running log of every ARIA cycle.
    Append-only. Each line is a JSON record.
    This is what ARIA uses to reflect and improve.
    """

    def __init__(self):
        EPISODIC_FILE.parent.mkdir(exist_ok=True)
        logger.debug(f"Episodic memory: {EPISODIC_FILE}")

    def write(self, cycle: int, percept: dict, action: str,
              outcome: str, emotion: str):
        record = {
            "timestamp": datetime.now().isoformat(),
            "cycle":     cycle,
            "percept":   percept,
            "action":    action,
            "outcome":   outcome,
            "emotion":   emotion,
        }
        with open(EPISODIC_FILE, "a") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Episodic write: cycle {cycle} → {action} → {outcome}")

    def read_last(self, n: int = 10) -> list:
        if not EPISODIC_FILE.exists():
            return []
        with open(EPISODIC_FILE) as f:
            lines = f.readlines()
        records = [json.loads(l) for l in lines[-n:]]
        logger.debug(f"Episodic read: last {len(records)} records")
        return records

    def count(self) -> int:
        if not EPISODIC_FILE.exists():
            return 0
        with open(EPISODIC_FILE) as f:
            return sum(1 for _ in f)
