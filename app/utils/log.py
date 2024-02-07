import sys
from loguru import logger

log = logger
logger.remove()


def disable_logging():
    log.warning(
        "Logging disabled due to performance reasons and security concerns ❗️❗️❗️"
    )
    log.remove()
    return


def enable_console_logging():
    log.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> | <cyan>{process.name}:{process.id}</cyan> | <cyan>{thread.name}</cyan> | <cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
        enqueue=True,
    )
    # log.success("Console logging enabled")
    return


enable_console_logging()
