import os.path
from typing import List
from ruamel import yaml

from .constants import core_constant

CONFIG_FILE = 'config.yml'


class Config:
    token: str
    plugin_directories: List[str]
    log_level: str

    def __init__(self, **kwargs) -> None:
        self.token = kwargs.get('token', '')
        self.plugin_directories = kwargs.get('plugin_directories', [])
        self.log_level = kwargs.get('log_level', 'INFO')

    @classmethod
    def load(cls, logger):
        if not os.path.exists(CONFIG_FILE):
            logger.error(f'config.yml was not found. '
                         f'Use "python -m {core_constant.PACKAGE_NAME} init" to generate default config file.')
            raise FileNotFoundError('config.yml was not found.')
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return cls(**yaml.round_trip_load(f))
