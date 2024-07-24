"""All functions and features for logging the app
"""
import sys
from loguru import logger

def init_logging(log_level: str) -> None:
    """Initialization of logging to create log file and set level at beginning of the app.

    Args:
        log_level (str): Configured log level
    """
    logger.remove()
    logger.add("../files/henCommander.log", rotation="500 MB", level=log_level)
    logger.add(sys.stdout, colorize=True, level=log_level)
