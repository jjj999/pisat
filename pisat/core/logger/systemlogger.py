
import logging
from logging import FileHandler, Formatter, LogRecord, Logger
from typing import Optional, Union

from pisat.base.component import Component
from pisat.util.about_time import get_time_stamp


class SystemLogger(Component):

    FORMAT_DEFAULT = "%(levelname)s : %(asctime)s : %(message)s"
    FILE_NAME_DEFAULT = "systemlog"
    FILE_EXTENSION_DEFAULT = "log"

    def __init__(self,
                 lname: Optional[str] = None,
                 level: Union[int, str] = logging.INFO,
                 name: Optional[str] = None) -> None:

        super().__init__(name=name)
        self._logger: Logger = logging.getLogger(name=lname)
        self._logger.setLevel(level)
        self.fhandler: Optional[FileHandler] = None

    def setLevel(self, level):
        self._logger.setLevel(level)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self._logger.warn(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info: bool = True, **kwargs):
        self._logger.exception(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self._logger.log(level, msg, *args, **kwargs)

    def findCaller(self, stack_info: bool = False):
        return self._logger.findCaller(stack_info)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None) -> LogRecord:
        return self._logger.makeRecord(name, level, fn, lno, msg, args, exc_info,
                                       func=func, extra=extra, sinfo=sinfo)

    def handle(self, record):
        self._logger.handle(record)

    def addHandler(self, hdlr):
        self._logger.addHandler(hdlr)

    def removeHandler(self, hdlr):
        self._logger.removeHandler(hdlr)

    def hasHandlers(self) -> bool:
        return self._logger.hasHandlers()

    def getEffectiveLevel(self) -> int:
        return self._logger.getEffectiveLevel()

    def isEnabledFor(self, level) -> bool:
        return self._logger.isEnabledFor(level)

    def getChild(self, suffix) -> Logger:
        return self._logger.getChild(suffix)

    def setFileHandler(self,
                       filename: Optional[str] = None,
                       level: int = logging.INFO,
                       fmt: Optional[str] = None,
                       mode: str = "a",
                       encoding: Optional[str] = None,
                       delay: bool = True):

        if filename is None:
            filename = get_time_stamp(
                self.FILE_NAME_DEFAULT, self.FILE_EXTENSION_DEFAULT)

        if fmt is not None:
            formatter = Formatter(fmt)
        else:
            formatter = Formatter(self.FORMAT_DEFAULT)

        self.fhandler = FileHandler(
            filename, mode=mode, encoding=encoding, delay=delay)
        self.fhandler.setLevel(level)
        self.fhandler.setFormatter(formatter)
        self._logger.addHandler(self.fhandler)

    def close(self):
        if self.fhandler is not None:
            self.fhandler.flush()
            self.fhandler.close()
