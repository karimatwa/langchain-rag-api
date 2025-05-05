# logger.py
import logging
import sys
from typing import Optional

class Logger:
    """
    Simple wrapper around Python's logging to provide a pre-configured logger.
    Usage:
        from logger import Logger
        logger = Logger.get(__name__)
        logger.info("Hello world")
    """

    _configured = False

    @staticmethod
    def configure(
        level: int = logging.INFO,
        fmt: str = "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt: str = "%Y-%m-%d %H:%M:%S",
        to_console: bool = True,
        logfile: Optional[str] = None
    ) -> None:
        """
        Call once at application startup to configure the root logger.
        - level:    minimum level to log (DEBUG, INFO, WARNING, ERROR)
        - fmt:      log line format
        - datefmt:  timestamp format
        - to_console: whether to emit to stdout
        - logfile:  if set, also emit to this file
        """
        if Logger._configured:
            return
        Logger._configured = True

        handlers = []
        if to_console:
            console_h = logging.StreamHandler(sys.stdout)
            handlers.append(console_h)
        if logfile:
            file_h = logging.FileHandler(logfile)
            handlers.append(file_h)

        logging.basicConfig(
            level=level,
            format=fmt,
            datefmt=datefmt,
            handlers=handlers
        )

    @staticmethod
    def get(name: str) -> logging.Logger:
        """
        Returns a logger with the given name. Make sure configure() has
        already been called (e.g. at program entry).
        """
        return logging.getLogger(name)
