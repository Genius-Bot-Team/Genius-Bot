import asyncio
import os.path
import pkgutil

from khl import Bot

from .bot_state import GeniusBotState
from .config import Config


class GeniusBot(Bot):

    def __init__(self, *, initialize_environment: bool = False, generate_default_only: bool = False) -> None:
        self.bot_state = GeniusBotState.INITIALIZING

        self.config = Config.load()

        # --- Input arguments "generate_default_only" processing --- #
        if generate_default_only:
            data = pkgutil.get_data('geniusbot', 'resources/default_config.yml')
            with open('config.yml', 'wb') as f:
                f.write(data)
            return

        # --- Initialize fields instance --- #
        if initialize_environment:
            if not os.path.exists('config.yml'):
                data = pkgutil.get_data('geniusbot', 'resources/default_config.yml')
                with open('config.yml', 'wb') as f:
                    f.write(data)
            if not os.path.exists('plugins'):
                os.mkdir('plugins')
            if not os.path.exists('config'):
                os.mkdir('config')
            return

        super().__init__(self.config.token)

    def start_bot(self):
        if not self.loop:
            self.loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            # do something when bot stopped
            ...

    # state

    def bot_in_state(self, state: GeniusBotState) -> bool:
        return self.bot_state.in_state(state)

    def is_initialized(self) -> bool:
        return self.bot_in_state(GeniusBotState.INITIALIZED)

    def set_bot_state(self, state: GeniusBotState):
        self.bot_state = state
