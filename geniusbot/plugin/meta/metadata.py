import re
from typing import Optional, TYPE_CHECKING, List, Dict, Any, Type, Union, Iterable

from geniusbot.plugin.meta.version import Version, VersionRequirement, VersionParsingError

if TYPE_CHECKING:
    from ..type.plugin import AbstractPlugin


class MetaData:
    id: str
    version: Version
    name: str
    description: Optional[str]
    author: Optional[List[str]]
    link: Optional[str]
    dependencies: Optional[Dict[str, VersionRequirement]]

    def __init__(self, data: Optional[dict], *, plugin: Optional['AbstractPlugin'] = None) -> None:
        if not isinstance(data, dict):
            data = {}

        def warn(*args, **kwargs):
            if plugin is not None:
                plugin.bot.logger.warning(*args, **kwargs)

        plugin_name_text = repr(plugin)

        use_fallback_id_reason = None
        self.id = data.get('id')
        if self.id is None:
            use_fallback_id_reason = f'Plugin ID of {plugin_name_text} not found'
        elif not isinstance(self.id, str) or re.fullmatch(r'[a-z0-9_]{1,64}', self.id) is None:
            use_fallback_id_reason = f'Plugin ID "{self.id}" of {plugin_name_text} is invalid'
        if use_fallback_id_reason is not None:
            if plugin is not None:
                self.id = plugin.get_fallback_metadata_id()
                warn('{}, use fallback id {} instead'.format(use_fallback_id_reason, self.id))
            else:
                raise ValueError('Plugin id not found in metadata')
        check_type(self.id, str)

        self.name = data.get('name', self.id)
        check_type(self.name, str)

        self.description = data.get('description')
        check_type(self.description, [type(None), str, dict])

        self.author = data.get('author')
        if isinstance(self.author, str):
            self.author = [self.author]
        if isinstance(self.author, list):
            for i in range(len(self.author)):
                self.author[i] = str(self.author[i])
            if len(self.author) == 0:
                self.author = None
        check_type(self.author, [type(None), list])

        self.link = data.get('link')
        check_type(self.link, [type(None), str])

        version_str = data.get('version')
        if version_str:
            try:
                self.version = Version(version_str, allow_wildcard=False)
            except VersionParsingError as e:
                warn(f'Version "{version_str}" of {plugin_name_text} is invalid ({e}), '
                     f'ignore and use fallback version instead 0.0.0')
        else:
            warn(f'{plugin_name_text} doesn\'t specific a version, use fallback version 0.0.0')
        if version_str is None:
            self.version = Version('0.0.0')

        self.dependencies = {}
        for plugin_id, requirement in data.get('dependencies', {}).items():
            try:
                self.dependencies[plugin_id] = VersionRequirement(requirement)
            except VersionParsingError as e:
                warn(f'Dependency "{plugin_id}: {requirement}" of {plugin_name_text} is invalid ({e}), ignore')

    def __repr__(self) -> str:
        return f'{type(self).__name__}[{",".join([f"{k}={repr(v)}" for k, v in vars(self).items() if not k.startswith("_")])}]'

    def get_description(self) -> Optional[str]:
        return self.description


__SAMPLE_METADATA = {
    'id': 'example_plugin',  # If missing it will be the file name without .py suffix
    'version': '1.0.0',  # If missing it will be '0.0.0'
    'name': 'Sample Plugin',
    'description': "Sample plugin for Genius-Bot",
    'author': [
        'DancingSnow'
    ],
    'link': 'https://github.com/Genius-Bot-Team/Genius-Bot',
    'dependencies': {
        'gbot': '>=1.0.0'
    }
}


def check_type(value: Any, types: Union[Type, Iterable[Type]], error_message: str = None):
    if not isinstance(types, Iterable):
        types = [types]
    if not any(map(lambda t: isinstance(value, t), types)):
        if error_message is None:
            error_message = 'Except type {} but found type {}'.format(types, type(value))
        raise TypeError(error_message)
