import requests


class WordCountDao:

    @staticmethod
    def send_word_count(word_frequency):
        url = "INSERT ENDPOINT FROM ENV VARIABLE"

        res = requests.post(url, data=word_frequency)

        print(res)

        return True
