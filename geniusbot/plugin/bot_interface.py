import functools
from typing import TYPE_CHECKING, Optional, Union

from khl import Channel
from khl_card import CardMessage

from .type.plugin import AbstractPlugin
from ..utils.logger import GeniusBotLogger

if TYPE_CHECKING:
    from ..genius_bot import GeniusBot


class BotInterface:
    __global_instance: Optional['BotInterface'] = None  # For singleton instance storage

    def __init__(self, bot: 'GeniusBot') -> None:
        self._bot = bot
        if BotInterface.__global_instance is not None:
            self._bot.logger.warning(f'Double assigning the singleton instance in {self.__class__.__name__}',
                                     stack_info=True)
        BotInterface.__global_instance = self

    @functools.lru_cache(maxsize=512, typed=True)
    def _get_logger(self, plugin_id: str) -> GeniusBotLogger:
        logger = GeniusBotLogger(plugin_id)
        logger.addHandler(self._bot.logger.file_handler)
        return logger

    @property
    def logger(self) -> GeniusBotLogger:
        return self._bot.logger

    # utils

    @classmethod
    def get_instance(cls) -> Optional['BotInterface']:
        return BotInterface.__global_instance

    # Bot Control

    def stop_bot(self):
        raise KeyboardInterrupt

    async def send(self, channel: Union[str, Channel], msg: Union[str, list, CardMessage], **kwargs):
        channel = channel if isinstance(channel, Channel) else await self._bot.client.fetch_public_channel(channel)
        if isinstance(msg, CardMessage):
            await self._bot.client.send(channel, msg.build(), **kwargs)
        else:
            await self._bot.client.send(channel, msg, **kwargs)


class PluginBotInterface(BotInterface):

    def __init__(self, bot: 'GeniusBot', plugin: AbstractPlugin) -> None:
        super().__init__(bot)
        self.__plugin = plugin
        self.__logger_for_plugin = None

    @property
    def logger(self) -> GeniusBotLogger:
        if self.__logger_for_plugin is None:
            try:
                logger = self._get_logger(self.__plugin.get_id())
            except:
                logger = self._bot.logger
            self.__logger_for_plugin = logger
        return self.__logger_for_plugin



