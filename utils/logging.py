import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)


class LogF:
    @staticmethod
    def log(text: str):
        datetime.now()
        logger.warning(str(datetime.now()) + " | " + text)
