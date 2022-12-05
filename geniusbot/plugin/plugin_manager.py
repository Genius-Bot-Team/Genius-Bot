from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from ..genius_bot import GeniusBot


class PluginManager:
    def __init__(self, bot: 'GeniusBot') -> None:
        self.bot = bot
        self.logger = self.bot.logger
        self.plugin_directories: List[str] = []

        self.plugins: Dict[str, 'Plugin'] = {}  # plugin_id <-> Plugin
        self.plugin_file_path: Dict[str, str] = {}  # plugin_id <-> plugin path

    def get_plugin_amount(self) -> int:
        ...

    def get_all_plugins(self) -> List['Plugin']:
        ...

    def get_plugin_by_id(self, plugin_id: str) -> 'Plugin':
        ...

    def __load_plugin(self, file_path):
        ...

    def __unload_plugin(self, plugin: 'Plugin'):
        ...

    def __reload_plugin(self, plugin: 'Plugin'):
        ...

    def __collect_possible_plugin_file_paths(self) -> List[str]:
        ...

    # Interfaces

    def load_plugin(self, file_path):
        ...

    def unload_plugin(self, plugin: 'Plugin'):
        ...

    def reload_plugin(self, plugin: 'Plugin'):
        ...

    def enable_plugin(self, file_path):
        ...

    def disable_plugin(self, plugin: 'Plugin'):
        ...

    def refresh_all_plugins(self):
        ...

    def refresh_changed_plugins(self):
        ...
