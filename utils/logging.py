import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

class LogF:
    """
    Class for handling all kinds of logging.
    """

    @staticmethod
    def log(text: str):
        """
        Outputs a timestamp as well as a message to the console.

        :param text: The message to print
        """
        datetime.now()
        logger.warning(str(datetime.now()) + " | " + text)
