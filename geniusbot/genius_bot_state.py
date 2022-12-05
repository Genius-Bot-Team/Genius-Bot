from enum import Enum
from typing import Iterable


class GeniusBotState(Enum):
    INITIALIZING = 'initializing'    # Just entered construction method
    INITIALIZED = 'initialized'      # Construction finished
    RUNNING = 'running'              # Genius-Bot started and is running
    PRE_STOPPED = 'pre_stopped'      # Genius-Bot is stopping and making some cleaning things
    STOPPED = 'stoped'               # Genius-Bot is stopped

    def in_state(self, states) -> bool:
        if type(states) is type(self):
            return states is self
        elif not isinstance(states, Iterable):
            states = (states,)
        return self in states
