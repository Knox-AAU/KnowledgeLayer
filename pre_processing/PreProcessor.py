import requests
from knox_source_data_io.models.publication import Paragraph, Publication
import exceptions
from environment import EnvironmentVariables as Ev
from model import Document
import logging

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)


class PreProcessor:
    """

    """
    def lemmatize(self, content: str, language: str) -> str:
        """
        Post's to the lemmatizer API defined in the environment (Ev)
        :param content: str - The content to be lemmatized
        :return: str - The lemmatized content
        """
        try:
            endpoint: str = Ev.instance.get_value(Ev.instance.LEMMATIZER_ENDPOINT)
            # TODO Add language when those gosh darn lemmatizer people get it back
            response: requests.Response = requests.post(endpoint, json={'string': content})
            response.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout) as e:
            raise exceptions.PostFailedException("ERROR: Error contacting Lemmatize API", e.response)
        except:
            raise exceptions.UnparsableException("ERROR: Unparseable by Lemmatize API")
        return response.json()['lemmatized_string']

    def process(self, document: Document) -> Document:
        print("Not overridden")
