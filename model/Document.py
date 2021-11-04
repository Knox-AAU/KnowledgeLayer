from typing import List


class Article:
    """
    An article is a general term and is used to either express a Grundfos manual or a Nordjyske article for example
    """

    def __init__(self, title, body, path):
        """

        :param title: Title of the article
        :param body: Text of the article
        :param path: The filepath to where the original file is located
        """
        self.title = title
        self.body = body
        self.path = path


class Document:
    """
    A general class intended to be compatiable with all data sources including data from Grundfos and Nordjyske
    """

    def __init__(self, publisher: str):
        """
        :param publisher: Examples: Grundfos, Nordjyske
        """
        self.publisher = publisher
        self.articles: List[Article] = []
