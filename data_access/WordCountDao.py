import requests
from environment import EnvironmentVariables as Ev


class WordCountDao:

    @staticmethod
    def send_word_count(word_frequency):
        url = Ev.instance.get_value(Ev.instance.WORD_COUNT_DATA_ENDPOINT)

        # TODO: Do error handling, since connection errors crashes the application
        res = requests.post(url, data=word_frequency)

        print(res)

        return True
