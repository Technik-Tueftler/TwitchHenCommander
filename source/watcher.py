from loguru import logger

logger.add("../files/henCommander.log", rotation="500 MB", level="INFO")

temp = 4/0