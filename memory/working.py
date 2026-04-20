from foundation.logger import get_logger

logger = get_logger("MEMORY")

class WorkingMemory:
    """
    Short-term memory for the current ARIA session.
    Holds the active context window — what ARIA is
    currently aware of. Cleared between sessions.
    """

    def __init__(self):
        self._state = {
            "cycle":        0,
            "last_speech":  None,
            "last_action":  None,
            "last_percept": None,
            "emotion":      "idle",
            "notes":        [],
        }
        logger.debug("Working memory initialised")

    def update(self, key: str, value):
        self._state[key] = value
        logger.debug(f"Working memory: {key} = {value}")

    def get(self, key: str, default=None):
        return self._state.get(key, default)

    def increment_cycle(self):
        self._state["cycle"] += 1
        return self._state["cycle"]

    def add_note(self, note: str):
        self._state["notes"].append(note)
        logger.debug(f"Working memory note: {note}")

    def snapshot(self) -> dict:
        return dict(self._state)

    def clear(self):
        cycle = self._state["cycle"]
        self.__init__()
        self._state["cycle"] = cycle
        logger.debug("Working memory cleared")
