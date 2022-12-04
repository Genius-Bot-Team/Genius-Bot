import os.path
from typing import List
from ruamel import yaml

CONFIG_FILE = 'config.yml'


class Config:
    token: str
    plugin_directories: List[str]

    def __init__(self, **kwargs) -> None:
        self.token = kwargs.get('token', '')
        self.plugin_directories = kwargs.get('plugin_directories', [])

    @classmethod
    def load(cls):
        if not os.path.exists(CONFIG_FILE):
            return cls()
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return cls(**yaml.round_trip_load(f))
