import json
from pathlib import Path
from foundation.logger import get_logger

logger = get_logger("MEMORY")

SEMANTIC_FILE = Path(__file__).parent.parent / "logs" / "semantic.json"

class SemanticMemory:
    """
    Long-term knowledge store.
    Persists across sessions — preferences, environment
    facts, learned behaviours, named entities.
    """

    def __init__(self):
        SEMANTIC_FILE.parent.mkdir(exist_ok=True)
        if SEMANTIC_FILE.exists():
            with open(SEMANTIC_FILE) as f:
                self._store = json.load(f)
        else:
            self._store = {}
        logger.debug(f"Semantic memory loaded: {len(self._store)} entries")

    def set(self, key: str, value):
        self._store[key] = value
        self._save()
        logger.debug(f"Semantic set: {key} = {value}")

    def get(self, key: str, default=None):
        value = self._store.get(key, default)
        logger.debug(f"Semantic get: {key} = {value}")
        return value

    def delete(self, key: str):
        if key in self._store:
            del self._store[key]
            self._save()
            logger.debug(f"Semantic delete: {key}")

    def all(self) -> dict:
        return dict(self._store)

    def _save(self):
        with open(SEMANTIC_FILE, "w") as f:
            json.dump(self._store, f, indent=2)
