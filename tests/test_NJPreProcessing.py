from typing import List
import pytest
from unittest.mock import patch
import unittest

import requests.exceptions
import spacy.lang.da

import exceptions
from model.Document import Document, Article
from pre_processing import NJPreProcessor
from knox_source_data_io.models.publication import Publication, Paragraph
from knox_source_data_io.models.wrapper import Wrapper, Generator

xfail = pytest.mark.xfail


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.preproc = NJPreProcessor()

    def create_article(self, title: str, body: str) -> Article:
        return Article(title, body, "/testpath.extension")

    def setup_data(self, articleBodies: List[str]) -> Document:
        makeArticle = lambda title, body: Article(title, body, "/testpath.extension")
        document = Document("Test Publisher")
        document.articles = [makeArticle(f'TestTitle Nr. {i}', v) for i, v in enumerate(articleBodies)]
        return document

    @patch('pre_processing.PreProcessor.lemmatize')
    def test__process__removes_stopwords(self, mock_post):
        # Arrange
        data = self.setup_data(["hej, jeg vil gerne. testes..,"])
        mock_post.side_effect = lambda x, y: x

        # Act
        output = self.preproc.process(data).articles[0].body

        # Assert
        self.assertEqual("hej gerne testes", output)

    @patch('pre_processing.PreProcessor.lemmatize')
    def test__process__removes_stopwords_multiple(self, mock_post):
        # Arrange
        data = self.setup_data(["hej, jeg vil gerne. testes..,", "hej, jeg vil gerne. testes.., I. DAG. TAK."])
        mock_post.side_effect = lambda x, y: x

        # Act
        output = [p.body for p in self.preproc.process(data).articles]

        # Assert
        self.assertEqual(["hej gerne testes", "hej gerne testes I dag tak"], output)


    @patch('pre_processing.PreProcessor.lemmatize')
    def test__process__convert_to_modern_danish_works(self, mock_post):
        # Arrange
        data = self.setup_data(["hej, jeg vil gerne. testes..,", "hej, Rumskibet Karsten vil. testes.., I. DAG. TAK."])
        mock_post.side_effect = lambda x, y: x

        # Act
        output = [p.body for p in self.preproc.process(data).articles]

        # Assert
        self.assertEqual(["hej gerne testes", "hej rumskibet Karsten testes I dag tak"], output)

    @patch('pre_processing.PreProcessor.lemmatize')
    def test__process__lemmatize(self, mock_post):
        # Arrange
        data = self.setup_data(["tanken er fyldt op"])
        mock_post.return_value = "tanken fyldet op"

        # Act
        output = self.preproc.process(data).articles[0].body

        # Assert
        self.assertEqual("tanken fyldet op", output)

    @patch('requests.post')
    def test__process__lemmatize_raise_unparseable(self, mock_post):
        # Arrange
        data = self.setup_data(["tanken er fyldt op"])
        mock_post.side_effect = lambda x, y: (_ for _ in ()).throw(requests.exceptions.InvalidSchema())

        # Act & Assert
        with self.assertRaises(exceptions.UnparsableException) as ctx:
            self.preproc.process(data)

    # @patch('requests.post')
    # def test__process__lemmatize_raise_postFailed(self, mock_post):
    #     # Arrange
    #     data = self.setup_data(["tanken er fyldt op"])
    #     mock_post.side_effect = lambda x, y: (_ for _ in ()).throw(requests.exceptions.ConnectionError())
    #
    #     # Act & Assert
    #     with self.assertRaises(exceptions.PostFailedException):
    #         self.preproc.process(data)
