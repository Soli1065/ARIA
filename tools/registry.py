from foundation.logger import get_logger
from expression.mock import speak, move, express, stop
from memory.working import WorkingMemory
from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory

logger = get_logger("DISPATCHER")

class ToolDispatcher:
    """
    ARIA's action registry.
    Every tool ARIA can call is registered here.
    The LLM returns a tool name → dispatcher executes it.
    Adding new capabilities = registering a new tool.
    """

    def __init__(self, working: WorkingMemory,
                 episodic: EpisodicMemory,
                 semantic: SemanticMemory):
        self.working  = working
        self.episodic = episodic
        self.semantic = semantic

        self._tools = {
            # ── Expression ────────────────────────────────
            "speak":            self._speak,
            "move":             self._move,
            "express":          self._express,
            "stop":             self._stop,

            # ── Memory ────────────────────────────────────
            "remember":         self._remember,
            "recall":           self._recall,

            # ── Introspection ─────────────────────────────
            "observe":          self._observe,
            "reflect":          self._reflect,

            # ── Idle ──────────────────────────────────────
            "idle":             self._idle,
        }
        logger.info(f"Tool registry loaded: {len(self._tools)} tools available")

    # ── Dispatch ──────────────────────────────────────────

    def dispatch(self, tool: str, **kwargs) -> str:
        if tool not in self._tools:
            logger.warning(f"Unknown tool requested: '{tool}' — falling back to idle")
            tool = "idle"
        logger.info(f"Dispatching: {tool}({kwargs})")
        result = self._tools[tool](**kwargs)
        self.working.update("last_action", tool)
        return result

    def available_tools(self) -> list:
        return list(self._tools.keys())

    # ── Tool implementations ──────────────────────────────

    def _speak(self, text: str = "", **_) -> str:
        speak(text)
        self.working.update("last_speech", text)
        return f"spoke: {text}"

    def _move(self, action: str = "idle", **kwargs) -> str:
        move(action, **kwargs)
        return f"moved: {action}"

    def _express(self, emotion: str = "idle", **_) -> str:
        express(emotion)
        self.working.update("emotion", emotion)
        return f"expressed: {emotion}"

    def _stop(self, **_) -> str:
        stop()
        return "stopped"

    def _remember(self, key: str = "", value=None, **_) -> str:
        if key:
            self.semantic.set(key, value)
            return f"remembered: {key} = {value}"
        return "remember failed: no key provided"

    def _recall(self, key: str = "", **_) -> str:
        value = self.semantic.get(key)
        result = f"{key} = {value}" if value else f"{key} not found"
        logger.info(f"Recall: {result}")
        return result

    def _observe(self, **_) -> str:
        snapshot = self.working.snapshot()
        logger.info(f"Observation: {snapshot}")
        return str(snapshot)

    def _reflect(self, **_) -> str:
        records = self.episodic.read_last(5)
        summary = f"Last {len(records)} cycles reviewed"
        logger.info(f"Reflection: {summary}")
        self.working.add_note(summary)
        return summary

    def _idle(self, **_) -> str:
        express("idle")
        return "idling"
