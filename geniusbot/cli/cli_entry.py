import sys
from argparse import ArgumentParser

from ..constants import core_constant


def environment_check():
    """
    check python version
    """
    python_version = sys.version_info.major + sys.version_info.minor * 0.1
    if python_version < 3.6:
        print('Python 3.6+ is needed')
        raise Exception('Python version {} is too old'.format(python_version))


def entry_point():
    environment_check()
    if len(sys.argv) == 1:
        run_gbot()
        return

    parser = ArgumentParser(
        prog=core_constant.NAME_SHORT,
        description=f'{core_constant.NAME} CLI'
    )
    subparsers = parser.add_subparsers(title='Command', help='Available commands', dest='subparser_name')

    subparsers.add_parser('start', help=f'Start {core_constant.NAME}')
    subparsers.add_parser('init', help=f'Prepare the working environment of {core_constant.NAME}. '
                                       f'Create commonly used folders and generate default configuration')
    subparsers.add_parser('gendefault', help='Generate default configuration files at current working directory. '
                                             'Existed files will be overwritten')

    result = parser.parse_args()
    if result.subparser_name == 'start':
        run_gbot()
    elif result.subparser_name == 'init':
        initialize_environment()
    elif result.subparser_name == 'gendefault':
        generate_default_stuffs()


def run_gbot():
    """
    run the Genius-Bot
    """
    print('{} {} is starting up'.format(core_constant.NAME, core_constant.VERSION))


def initialize_environment():
    ...


def generate_default_stuffs():
    ...
