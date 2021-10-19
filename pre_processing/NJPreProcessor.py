import exceptions
from environment.EnvironmentConstants import EnvironmentVariables as Ev
Ev()
import spacy
from spacy.lang.da.stop_words import STOP_WORDS
import re
import requests
from knox_source_data_io.models.wrapper import Wrapper
from knox_source_data_io.models.publication import Paragraph, Publication


class NJPreProcessor:
    """

    """

    def __init__(self):
        self.nlp = spacy.load(Ev.instance.get_value(Ev.instance.NJ_SPACY_MODEL))

    def process(self, data: Wrapper) -> Wrapper:
        """
        Takes a Wrapper object and applies two preprocessing steps to it, removal of stop words and lemmatization.
        :param data: Wrapper
        :return: Wrapper
        """
        try:
            self.remove_stopwords(data.content)
            self.lemmatize(data.content)
        except exceptions.PostFailedException as e:
            raise e
        except Exception as e:
            raise exceptions.UnparsableException(e.message)
        return data

    def remove_stopwords(self, data: Publication) -> None:
        """
        :param data: Publication
        :return: None
        """
        for i in range(len(data.articles)):
            data.articles[i].paragraphs = [self.remove_paragraph_stopwords(p) for p in data.articles[i].paragraphs]

    def remove_paragraph_stopwords(self, paragraph: Paragraph) -> Paragraph:
        """
        :param paragraph: Paragraph - A Paragraph containing to content to be filtered.
        :return: Paragraph - The processed Paragraph

        This function will filter out all danish stopwords
        Furthermore, commas and periods will be removed, as these are included as stopwords
        (see: https://ordnet.dk/ddo/ordbog?query=stopord)
        """
        content = re.sub(r'(\[\d+\])|[.,?]', '', paragraph.value)

        # Filter out stopwords
        return_word_list = [i for i in content.split(' ') if i not in STOP_WORDS]
        paragraph.value = ' '.join(word for word in return_word_list)
        return paragraph

    def convert_to_modern_danish(self, data: Publication) -> None:
        """

        :param content: Publication
        :return: None
        """
        pass

    def lemmatize(self, data: Publication) -> None:
        """
        :param data: Publication - The publication to be lemmatized
        :return: None
        """
        for i in range(len(data.articles)):
            data.articles[i].paragraphs = [Paragraph(kind=p.kind, value=self.call_lemmatize_api(p.value))
                                           for p in data.articles[i].paragraphs]

    def call_lemmatize_api(self, content: str) -> str:
        """
        Post's to the lemmatizer API defined in the environment (Ev)
        :param content: str - The content to be lemmatized
        :return: str - The lemmatized content
        """
        try:
            endpoint: str = Ev.instance.get_value(Ev.instance.LEMMATIZER_ENDPOINT)
            response: requests.Response = requests.post(endpoint, content)
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout) as e:
            raise exceptions.PostFailedException("ERROR: Error contacting Lemmatize API", e.response)
        except:
            raise exceptions.UnparsableException("ERROR: Unparseable by Lemmatize API")
        return response.json()
