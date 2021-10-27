from typing import List, Tuple

import exceptions
from environment.EnvironmentConstants import EnvironmentVariables as Ev
from model.Document import Document, Article

Ev()
import spacy
from spacy.lang.da.stop_words import STOP_WORDS
import re
import requests
from knox_source_data_io.io_handler import IOHandler, Generator
from knox_source_data_io.models.wrapper import Wrapper
from knox_source_data_io.models.publication import Paragraph, Publication
from .PreProcessor import PreProcessor
import json

class NJPreProcessor(PreProcessor):
    """

    """

    def __init__(self):
        self.nlp = spacy.load(Ev.instance.get_value(Ev.instance.NJ_SPACY_MODEL))
        self.io_handler = IOHandler(Generator(), "")

    def process(self, document: Document) -> Wrapper:
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
            document.articles = [self.process_article(article) for article in document.articles]
            # self.remove_stopwords(document)
            # self.convert_to_modern_danish(document)
            # self.lemmatize_publication(document)
        except Exception as e:
            raise e
        return document

    def process_article(self, article: Article):
        self.remove_stopwords(article)
        self.convert_to_modern_danish(article)
        article.body = super().lemmatize(article.body, "dk")
        return article
    # def remove_stopwords(self, document: Document) -> None:
    #     """
    #     :param data: Publication
    #     :return: None
    #     """
    #     document.articles = [self.remove_paragraph_stopwords(article) for article in document.articles]
    #     # for article in document.articles:
    #     #     article.body =
    #     #     article.paragraphs = [self.remove_paragraph_stopwords(paragraph) for paragraph in article.paragraphs]

    def remove_stopwords(self, article: Article) -> Article:
        """
        :param paragraph: Paragraph - A Paragraph containing to content to be filtered.
        :return: Paragraph - The processed Paragraph

        This function will filter out all danish stopwords
        Furthermore, commas and periods will be removed, as these are included as stopwords
        (see: https://ordnet.dk/ddo/ordbog?query=stopord)
        """
        content: str = re.sub(r'(\[\d+\])|[.,?]', '', article.body)
        # Filter out stopwords
        return_word_list: List[str] = [i for i in content.split(' ') if i not in STOP_WORDS]
        article.body = ' '.join(word for word in return_word_list)

        return article

    # def convert_to_modern_danish(self, document: Document) -> None:
    #     """
    #     :param data:
    #     :return: None
    #     """
    #     document.articles = [self.convert_paragraph_to_modern_danish(article) for article in document.articles]
    #     # for article in document.articles:
    #     #     article.paragraphs = [self.convert_paragraph_to_modern_danish(paragraph)
    #     #                           for paragraph in article.paragraphs]

    def convert_to_modern_danish(self, article: Article) -> Article:
        """
        Replaces aa, Aa, oe, Oe, aa, Aa -> æ, Æ, ø, Ø, å, Å as well as replacing any kind of whitespace with a single
        space. Also converts all NOUN's, as defined in spacy.lang.da.STOP_WORDS, to lowercase.

        :param paragraph: Paragraph - The paragraph to convert to modern danish
        :return: Paragraph - The processed paragraph
        """
        content: str = article.body

        replacements: List[Tuple[str, str]] = [(r'aa', 'å'), (r'Aa', 'Å'), (r'ei', 'ej'), (r'oe', 'ø'), (r'Øe', 'Ø'),
                                               (r'ae', 'æ'), (r'Ae', 'Æ'), (r'\-(\r?)\n', ''), (r'\r?\n', ' ')]
        for regex, sub in replacements:
            content = re.sub(regex, sub, content)

        lower_noun = lambda word: word.lower() if self.nlp(word)[0].pos_ == 'NOUN' else word
        words = [lower_noun(word) for word in re.split(r'\s+', content)]
        article.body = ' '.join(words)
        return article

    # def lemmatize_publication(self, document: Document) -> None:
    #     """
    #     :param data: Publication - The publication to be lemmatized
    #     :return: None
    #     """
    #     for article in data.articles:
    #         article.paragraphs = [Paragraph(kind=paragraph.kind, value=super().lemmatize(paragraph.value, "dk"))
    #                               for paragraph in article.paragraphs]
