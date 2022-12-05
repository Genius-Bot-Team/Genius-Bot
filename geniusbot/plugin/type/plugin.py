from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import TYPE_CHECKING

from ..bot_interface import PluginBotInterface
from ..meta.metadata import MetaData

if TYPE_CHECKING:
    from ..plugin_manager import PluginManager


class PluginState(Enum):
    UNINITIALIZED = auto()  # just created the instance
    LOADING = auto()  # loading the .py entrance file
    LOADED = auto()  # loaded the .py entrance file
    READY = auto()  # called "on load" event, ready to do anything
    UNLOADING = auto()  # just removed from the plugin list, ready to call "on unload" event
    UNLOADED = auto()  # unloaded, should never access it


class AbstractPlugin(ABC):

    def __init__(self, plugin_manager: 'PluginManager', file_path) -> None:
        self.plugin_manager = plugin_manager
        self.bot = plugin_manager.bot
        self.file_path = file_path
        self.state = PluginState.UNINITIALIZED

        self.bot_interface = PluginBotInterface(self.bot, self)

    @abstractmethod
    def get_metadata(self) -> MetaData:
        ...

    def get_id(self) -> str:
        return self.get_metadata().id

    def get_meta_name(self) -> str:
        return self.get_metadata().name

    @abstractmethod
    def get_fallback_metadata_id(self) -> str:
        ...

    def get_name(self) -> str:
        try:
            return self.get_identifier()
        except RuntimeError:
            return repr(self)

    def get_identifier(self) -> str:
        meta_data = self.get_metadata()
        return '{}@{}'.format(meta_data.id, meta_data.version)

    def __str__(self):
        return self.get_name()

    @abstractmethod
    def __repr__(self):
        ...

    # Plugin State
    def set_state(self, state):
        self.state = state

    def in_states(self, states):
        return self.state in states

    def assert_state(self, states, extra_message=None):
        if not self.in_states(states):
            msg = f'{repr(self)} state assertion failed, excepts {states} but founded {self.state}.'
            if extra_message is not None:
                msg += ' ' + extra_message
            raise RuntimeError(msg)

    # Life Cycle
    @abstractmethod
    def load(self):
        ...

    @abstractmethod
    def ready(self):
        ...

    @abstractmethod
    def reload(self):
        ...

    @abstractmethod
    def unload(self):
        ...

    @abstractmethod
    def remove(self):
        ...

    # Plugin Registry

    def __assert_allow_to_register(self, target):
        self.assert_state([PluginState.LOADED, PluginState.READY],
                          f'Only plugin in loaded or ready state is allowed to register {target}')

    def register_command(self):
        # TODO: CommandManager
        ...

    def register_help_message(self):
        # TODO: help message registry
        ...
