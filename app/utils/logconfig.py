import sys

from loguru import logger


def init_logger():
    log_level = "DEBUG"
    logger.remove()
    logger.add(level=log_level, sink=sys.stdout, backtrace=False)
    logger.add(
        level=30, sink="backend/logs/warnings.log", rotation="10 MB", backtrace=False
    )
    logger.add(
        level=40, sink="backend/logs/errors.log", rotation="10 MB", backtrace=False
    )
