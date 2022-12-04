import os
from geniusbot import core_constant
from setuptools import setup, find_packages

# === cheatsheet ===
# linux rm
# rm -rf build/ dist/ Genius_Bot.egg-info/
# powershell rm
# rm -path "build" -Recurse; rm -path "dist" -Recurse; rm -path "Genius_Bot.egg-info" -Recurse
# python setup.py sdist bdist_wheel
# python -m twine upload --repository testpypi dist/*
# python -m twine upload dist/*

NAME = core_constant.PACKAGE_NAME
VERSION = core_constant.VERSION_PYPI
DESCRIPTION = 'A kook bot framework base on khl.py'
URL = 'https://github.com/Genius-Bot-Team/Genius-Bot'
AUTHOR = 'DancingSnow'

CLASSIFIERS = [
    # https://pypi.org/classifiers/
    'Programming Language :: Python'
]

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as f:
    REQUIRED = [line for line in f.readlines() if not len(line.strip()) == 0]

print('REQUIRED = {}'.format(REQUIRED))

with open(os.path.join(here, 'README.md'), encoding='utf8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    include_package_data=True,
    classifiers=CLASSIFIERS
)
