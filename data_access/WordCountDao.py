import requests
from environment import EnvironmentVariables as Ev
from requests.exceptions import ConnectionError


class WordCountDao:
    """

    """

    @staticmethod
    def send_word_count(word_frequency):
        """

        :param word_frequency:
        :return:
        """

        print("Output to be sent:\n" + word_frequency)

        url = Ev.instance.get_value(Ev.instance.WORD_COUNT_DATA_ENDPOINT)

        # TODO: Do error handling, since connection errors crashes the application
        try:
            res = requests.post(url, data=word_frequency)
            print(res)
        except ConnectionError as error:
            print("Connection error: " + str(error))
        except Exception as error:
            print("Something unexpected happened: " + str(error))
            print("Error type: " + str(type(error)))

        return True