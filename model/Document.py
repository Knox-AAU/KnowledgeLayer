from typing import List


class Article:
    """

    """
    def __init__(self, title, body, path):
        self.title = title
        self.body = body
        self.path = path


class Document:
    """

    """
    def __init__(self, publisher: str):
        self.publisher = publisher
        self.articles: List[Article] = []
