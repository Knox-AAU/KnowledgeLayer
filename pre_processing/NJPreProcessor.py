from typing import List, Tuple

from environment.EnvironmentConstants import EnvironmentVariables as Ev
from model.Document import Document, Article
from utils import load_model

Ev()
import spacy
from spacy.lang.da.stop_words import STOP_WORDS
import re
from knox_source_data_io.io_handler import IOHandler, Generator
from .PreProcessor import PreProcessor


class NJPreProcessor(PreProcessor):
    """

    """

    def __init__(self):
        self.nlp = spacy.load('da_core_news_lg', disable=["lemmatizer"])
        self.io_handler = IOHandler(Generator(), "")

    def process(self, document: Document) -> Document:
        """
        Takes a Document object and applies three preprocessing steps to it, removal of stop words,
        conversion to modern Danish and lemmatization.
        :param document: Document
        :return: Document
        """
        if self.nlp is None:
            raise Exception("No spaCy model configured.")
        if self.nlp.lang != 'da':
            raise Exception("Function 'convert_to_modern_danish' requires a danish spaCy model.")

        try:
            document.articles = [self.process_article(article) for article in document.articles]
        except Exception as e:
            raise e
        return document

    def process_article(self, article: Article):
        self.remove_stopwords(article)
        self.convert_to_modern_danish(article)
        article.body = super().lemmatize(article.body, "dk")
        return article

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

    def convert_to_modern_danish(self, article: Article) -> Article:
        """
        Replaces aa, Aa, oe, Oe, aa, Aa -> æ, Æ, ø, Ø, å, Å as well as replacing any kind of whitespace with a single
        space. Also converts all NOUN's, as defined in spacy.lang.da.STOP_WORDS, to lowercase.

        :param article:
        """
        content: str = article.body

        replacements: List[Tuple[str, str]] = [(r'aa', 'å'), (r'Aa', 'Å'), (r'ei', 'ej'), (r'oe', 'ø'), (r'Øe', 'Ø'),
                                               (r'ae', 'æ'), (r'Ae', 'Æ'), (r'\-(\r?)\n', ''), (r'\r?\n', ' ')]
        for regex, sub in replacements:
            content = re.sub(regex, sub, content)

        #lower_noun = lambda word: word.lower() if self.nlp(word)[0].pos_ == 'NOUN' else word
        words = [self.lower_noun(word) for word in re.split(r'\s+', content)]
        article.body = ' '.join(words)
        return article

    def lower_noun(self, word):
        token = self.nlp(word)
        if len(token) > 0 and token[0].pos_ == 'NOUN':
            return word.lower()
        else:
            return word
