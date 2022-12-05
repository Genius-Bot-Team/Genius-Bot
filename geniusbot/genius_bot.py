import asyncio
import os.path
import pkgutil

from khl import Bot

from .command.command_manager import CommandManager
from .genius_bot_state import GeniusBotState
from .config import Config
from .constants import core_constant
from .plugin.plugin_manager import PluginManager
from .utils.logger import GeniusBotLogger


class GeniusBot(Bot):

    def __init__(self, *, initialize_environment: bool = False, generate_default_only: bool = False) -> None:
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

        self.bot_state = GeniusBotState.INITIALIZING

        self.logger = GeniusBotLogger()
        self.config = Config.load(self.logger)
        self.logger.setLevel(self.config.log_level)
        self.logger.set_file(core_constant.LOGGING_FILE)

        # Constructing fields
        self.plugin_manager = PluginManager(self)
        self.command_manager = CommandManager(self)

        super().__init__(self.config.token)

        # INITIALIZE DONE
        self.bot_state = GeniusBotState.INITIALIZED

    def start_bot(self):
        if not self.loop:
            self.loop = asyncio.get_event_loop()
        try:
            self.bot_state = GeniusBotState.RUNNING
            self.loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            self.bot_state = GeniusBotState.PRE_STOPPED
            self.stop_bot()
            self.bot_state = GeniusBotState.STOPPED

    def stop_bot(self):
        # do something when bot stopped

        # call on_unload for all loaded plugins
        ...

    # state
    def bot_in_state(self, state: GeniusBotState) -> bool:
        return self.bot_state.in_state(state)

    def is_initialized(self) -> bool:
        return self.bot_in_state(GeniusBotState.INITIALIZED)

    def set_bot_state(self, state: GeniusBotState):
        self.bot_state = state
