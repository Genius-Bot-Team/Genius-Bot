from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..genius_bot import GeniusBot


class CommandManager:

    def __init__(self, bot: 'GeniusBot') -> None:
        self.bot = bot

    def clear_command(self):
        ...

    def register_command(self,):
        ...

    def execute_command(self):
        ...
