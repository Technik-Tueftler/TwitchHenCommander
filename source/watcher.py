"""All functions and features for logging the app
"""
import sys
from functools import partialmethod
from loguru import logger


def init_logging(log_level: str) -> None:
    """Initialization of logging to create log file and set level at beginning of the app.

    Args:
        log_level (str): Configured log level
    """
    logger.remove()
    logger.level("EXTDEBUG", no=9, color="<bold><yellow>")
    logger.__class__.extdebug = partialmethod(logger.__class__.log, "EXTDEBUG")
    logger.add("../files/henCommander.log", rotation="500 MB", level=log_level)
    logger.add(sys.stdout, colorize=True, level=log_level)
