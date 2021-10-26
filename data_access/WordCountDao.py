import dataclasses
import json
from typing import List

import requests

from data_access.data_transfer_objects.DocumentWordCountDto import DocumentWordCountDto
from environment import EnvironmentVariables as Ev
from requests.exceptions import ConnectionError


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
            res = requests.post(url, data=dto_as_json)
            print(res)
        except ConnectionError as error:
            print("Connection error: " + str(error))
        except Exception as error:
            print("Something unexpected happened: " + str(error))
            print("Error type: " + str(type(error)))

        return True
    
