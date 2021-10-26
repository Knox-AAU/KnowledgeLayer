import requests
from environment import EnvironmentVariables as Ev

class PreProcessor:
    """

    """
    def lemmatize(self, text, language):
        """

        :return:
        """
        raise NotImplementedError

    def extract_all_text_from_paragraphs(self, data):
        """

        :param data:
        :return:
        """
        corpus = ""

        for article in data["content"]["articles"]:
            for paragraph in article["paragraphs"]:
                corpus += paragraph["value"] + " "

        return corpus

    def process(self, json_data):
        print("Not overridden")
