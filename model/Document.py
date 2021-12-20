from typing import List
from dataclasses import dataclass


@dataclass
class Byline:
    """

    """

    def __init__(self, name: str, email = None):
        self.name = name
        self.email = email


@dataclass
class Article:
    """
    Subpart of the Document object, encapsulating a single article.
    """

    def __init__(self, title: str, body: str, path: str, byline: Byline = None, article_id: str = None):
        """

        :param title: Title of the article (headline)
        :param body: All paragraphs of the article concatenated
        :param path: The filepath to the original file
        :param byline: The author of the article (Nordjyske)
        :param article_id: An ID assigned to the article
        """
        self.title = title
        self.body = body
        self.path = path
        self.byline = byline
        self._id = article_id


    @property
    def id(self):
        if self._id is not None:
            return self._id
        else:
            return str(hash(self.title + self.path))

    @id.setter
    def id(self, value):
        self._id = value

    @id.deleter
    def id(self):
        self._id = None


@dataclass
class Document:
    """
    Intermediary format for documents received from the Preprocessing Layer.
    """

    def __init__(self, publisher: str, publication: str = None, articles=None, date: str = None):
        """

        :param publisher: The publisher of the publication
        :param publication: Name of the publication (Nordjyske)
        :param articles: A list of article objects
        :param date: Release date of the document
        """
        if articles is None:
            articles = []
        self.publisher = publisher
        self.articles: List[Article] = articles
        self.publication = publication
        self.date = date
