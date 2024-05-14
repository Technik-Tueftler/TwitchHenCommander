"""All functions and features for logging the app
"""
from loguru import logger

def init_logging(log_level: str) -> None:
    """Initialization of logging to create log file and set level at beginning of the app.

    Args:
        log_level (str): Configured log level
    """
    logger.add("../files/henCommander.log", rotation="500 MB", level=log_level)
