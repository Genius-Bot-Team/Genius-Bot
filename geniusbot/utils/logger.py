import os.path
import sys
import time
import weakref
import logging
import zipfile
from logging import Logger, Formatter, LogRecord, FileHandler, StreamHandler
from threading import RLock
from typing import Optional, Set

from colorlog import ColoredFormatter

from .file_util import touch_directory
from .string_util import clean_console_color_code

from ..constants import core_constant


class SyncStdoutStreamHandler(StreamHandler):
    __write_lock = RLock()
    __instance_lock = RLock()
    __instances = weakref.WeakSet()  # type: Set[SyncStdoutStreamHandler]

    def __init__(self) -> None:
        super().__init__(sys.stdout)
        with self.__instance_lock:
            self.__instances.add(self)

    def emit(self, record: LogRecord) -> None:
        with self.__write_lock:
            super().emit(record)

    @classmethod
    def update_stdout(cls, stream=None):
        if stream is None:
            stream = sys.stdout
        with cls.__instance_lock:
            instances = list(cls.__instances)
        for inst in instances:
            inst.acquire()
            try:
                inst.stream = stream
            finally:
                inst.release()


class NoColorFormatter(Formatter):
    def formatMessage(self, record: LogRecord) -> str:
        return clean_console_color_code(super().formatMessage(record))


class GeniusBotLogger(Logger):
    DEFAULT_NAME = core_constant.NAME_SHORT
    LOG_COLORS = {
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
    SECONDARY_LOG_COLORS = {
        'message': {
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red'
        }
    }

    @property
    def __file_formatter(self):
        return NoColorFormatter(
            '[%(name)s] [%(asctime)s] [%(threadName)s/%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    @property
    def __console_formatter(self):
        extra = '' if self.__plugin_id is None else ' [{}]'.format(self.__plugin_id)
        return ColoredFormatter(
            f'[%(name)s] [%(asctime)s] [%(threadName)s/%(log_color)s%(levelname)s%(reset)s]{extra}: %(message_log_color)s%(message)s%(reset)s',
            log_colors=self.LOG_COLORS,
            secondary_log_colors=self.SECONDARY_LOG_COLORS,
            datefmt='%H:%M:%S'
        )

    def __init__(self, plugin_id: Optional[str] = None) -> None:
        super().__init__(self.DEFAULT_NAME)
        self.file_handler: Optional[FileHandler] = None
        self.__plugin_id = plugin_id

        self.console_handler = SyncStdoutStreamHandler()
        self.console_handler.setFormatter(self.__console_formatter)

        self.addHandler(self.console_handler)

    def set_file(self, file_name: str):
        if self.file_handler is not None:
            self.removeHandler(self.file_handler)
        touch_directory(os.path.dirname(file_name))
        if os.path.isfile(file_name):
            modify_time = time.strftime('%Y-%m-%d', time.localtime(os.stat(file_name).st_mtime))
            counter = 0
            while True:
                counter += 1
                zip_file_name = '{}/{}-{}.zip'.format(os.path.dirname(file_name), modify_time, counter)
                if not os.path.isfile(zip_file_name):
                    break
            zipf = zipfile.ZipFile(zip_file_name, 'w')
            zipf.write(file_name, arcname=os.path.basename(file_name), compress_type=zipfile.ZIP_DEFLATED)
            zipf.close()
            os.remove(file_name)
        self.file_handler = logging.FileHandler(file_name, encoding='utf8')
        self.file_handler.setFormatter(self.__file_formatter)
        self.addHandler(self.file_handler)

    def unset_file(self):
        if self.file_handler is not None:
            self.removeHandler(self.file_handler)
            self.file_handler.close()
            self.file_handler = None
