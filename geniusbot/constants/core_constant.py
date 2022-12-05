import os

NAME_SHORT = 'GBOT'
NAME = 'Genius-Bot'
PACKAGE_NAME = "geniusbot"

VERSION = '0.1.0'  # semver (1.2.3-alpha.4)
VERSION_PYPI = '0.1.0'  # pythonic ver (1.2.3a4)

GITHUB_URL = 'https://github.com/Genius-Bot-Team/Genius-Bot'

PACKAGE_PATH = os.path.realpath(os.path.join(os.path.dirname(__name__), '..'))

LOGGING_FILE = os.path.join('logs', f'{NAME_SHORT}.log')
