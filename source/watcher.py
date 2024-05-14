"""All functions and features for logging the app
"""
from loguru import logger

async def init_logging() -> None:
    """Initialization of logging to create log file and set level at beginning of the app.
    """
    logger.add("../files/henCommander.log", rotation="500 MB", level="INFO")
