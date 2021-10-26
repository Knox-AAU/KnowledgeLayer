from typing import List, Tuple

import exceptions
from environment.EnvironmentConstants import EnvironmentVariables as Ev

Ev()
import spacy
from spacy.lang.da.stop_words import STOP_WORDS
import re
from knox_source_data_io.models.wrapper import Wrapper
from knox_source_data_io.models.publication import Paragraph, Publication
from .PreProcessor import PreProcessor


class NJPreProcessor(PreProcessor):
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
        if self.nlp is None:
            raise Exception("No spaCy model configured.")
        if self.nlp.lang != 'da':
            raise Exception("Function 'convert_to_modern_danish' requires a danish spaCy model.")

        try:
            self.remove_stopwords(data.content)
            self.convert_to_modern_danish(data.content)
            self.lemmatize_publication(data.content)
        except exceptions.PostFailedException as e:
            raise e
        except Exception as e:
            if hasattr(e, 'message'):
                raise exceptions.UnparsableException(e.message)
            raise exceptions.UnparsableException("ERROR: Input unparseable")
        return data

    def remove_stopwords(self, data: Publication) -> None:
        """
        :param data: Publication
        :return: None
        """
        for article in data.articles:
            article.paragraphs = [self.remove_paragraph_stopwords(paragraph) for paragraph in article.paragraphs]

    def remove_paragraph_stopwords(self, paragraph: Paragraph) -> Paragraph:
        """
        :param paragraph: Paragraph - A Paragraph containing to content to be filtered.
        :return: Paragraph - The processed Paragraph

        This function will filter out all danish stopwords
        Furthermore, commas and periods will be removed, as these are included as stopwords
        (see: https://ordnet.dk/ddo/ordbog?query=stopord)
        """
        content: str = re.sub(r'(\[\d+\])|[.,?]', '', paragraph.value)
        # Filter out stopwords
        return_word_list: List[str] = [i for i in content.split(' ') if i not in STOP_WORDS]
        paragraph.value = ' '.join(word for word in return_word_list)

        return paragraph

    def convert_to_modern_danish(self, data: Publication) -> None:
        """
        :param data:
        :return: None
        """
        for article in data.articles:
            article.paragraphs = [self.convert_paragraph_to_modern_danish(paragraph)
                                  for paragraph in article.paragraphs]

    def convert_paragraph_to_modern_danish(self, paragraph: Paragraph) -> Paragraph:
        """
        Replaces aa, Aa, oe, Oe, aa, Aa -> æ, Æ, ø, Ø, å, Å as well as replacing any kind of whitespace with a single
        space. Also converts all NOUN's, as defined in spacy.lang.da.STOP_WORDS, to lowercase.

        :param paragraph: Paragraph - The paragraph to convert to modern danish
        :return: Paragraph - The processed paragraph
        """
        content: str = paragraph.value

        replacements: List[Tuple[str, str]] = [(r'aa', 'å'), (r'Aa', 'Å'), (r'ei', 'ej'), (r'oe', 'ø'), (r'Øe', 'Ø'),
                                               (r'ae', 'æ'), (r'Ae', 'Æ'), (r'\-(\r?)\n', ''), (r'\r?\n', ' ')]
        for regex, sub in replacements:
            content = re.sub(regex, sub, content)

        lower_noun = lambda word: word.lower() if self.nlp(word)[0].pos_ == 'NOUN' else word
        words = [lower_noun(word) for word in re.split(r'\s+', content)]
        paragraph.value = ' '.join(words)
        return paragraph

    def lemmatize_publication(self, data: Publication) -> None:
        """
        :param data: Publication - The publication to be lemmatized
        :return: None
        """
        for article in data.articles:
            article.paragraphs = [Paragraph(kind=paragraph.kind, value=super().lemmatize(paragraph.value, "dk"))
                                  for paragraph in article.paragraphs]
