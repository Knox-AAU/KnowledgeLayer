import dataclasses
import json
from typing import List

import requests

from data_access.data_transfer_objects.DocumentWordCountDto import DocumentWordCountDto
from environment import EnvironmentVariables as Ev
from requests.exceptions import ConnectionError
import logging

logger = logging.getLogger()
logger.warning(logging.NOTSET)

class WordCountDao:
    """

    """

    @staticmethod
    def send_word_count(documentWordCounts: List[DocumentWordCountDto]):
        """

        :param documentWordCounts:
        :return:
        """
        objects_as_dict = list(map(lambda x: dataclasses.asdict(x), documentWordCounts))
        dto_as_json = json.dumps(objects_as_dict)

        print("Output to be sent:\n" + dto_as_json)

        url = Ev.instance.get_value(Ev.instance.WORD_COUNT_DATA_ENDPOINT)

        # TODO: Do error handling, since connection errors crashes the application
        try:
            res = requests.post(url, json=dto_as_json)
            res.raise_for_status()
            print(res)
        except ConnectionError as error:
            logger.warning("Connection error: " + str(error))
            raise error
        except Exception as error:
            logger.warning("Something unexpected happened: " + str(error))
            logger.warning("Error type: " + str(type(error)))
            raise error

        return True
    
