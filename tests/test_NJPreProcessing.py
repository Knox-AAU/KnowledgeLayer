from typing import List
import pytest
from unittest.mock import patch
import unittest

import requests.exceptions
import spacy.lang.da

import exceptions
from pre_processing import NJPreProcessor
from knox_source_data_io.models.publication import Publication, Article, Paragraph
from knox_source_data_io.models.wrapper import Wrapper, Generator

xfail = pytest.mark.xfail


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.preproc = NJPreProcessor()

    def setup_data(self, paragraphs: List[str]) -> Wrapper:
        paragraph_instances = [Paragraph(kind="Text", value=v) for v in paragraphs]
        return Wrapper(
            type="test",
            schema="0.0.0",
            generator=Generator(app="test", version=1, generated_at="test"),
            content=Publication(
                publication="test inc",
                published_at="2021-12-12T12:12:12+0",
                publisher="Group C",
                pages=2,
                articles=[
                    Article(
                        id=1,
                        headline="En Test er Blevet Myrdet!",
                        paragraphs=paragraph_instances
                    )
                ]
            )
        )

    @patch('pre_processing.NJPreProcessor.call_lemmatize_api')
    def test__process__removes_stopwords(self, mock_post):
        # Arrange
        data = self.setup_data(["hej, jeg vil gerne. testes..,"])
        mock_post.side_effect = lambda x: x

        # Act
        output = self.preproc.process(data).content.articles[0].paragraphs[0].value

        # Assert
        self.assertEqual("hej gerne testes", output)

    @patch('pre_processing.NJPreProcessor.call_lemmatize_api')
    def test__process__removes_stopwords_multiple(self, mock_post):
        # Arrange
        data = self.setup_data(["hej, jeg vil gerne. testes..,", "hej, jeg vil gerne. testes.., I. DAG. TAK."])
        mock_post.side_effect = lambda x: x

        # Act
        output = [p.value for p in self.preproc.process(data).content.articles[0].paragraphs]

        # Assert
        self.assertEqual(["hej gerne testes", "hej gerne testes I dag tak"], output)


    @patch('pre_processing.NJPreProcessor.call_lemmatize_api')
    def test__process__convert_to_modern_danish_works(self, mock_post):
        # Arrange
        data = self.setup_data(["hej, jeg vil gerne. testes..,", "hej, Rumskibet Karsten vil. testes.., I. DAG. TAK."])
        mock_post.side_effect = lambda x: x

        # Act
        output = [p.value for p in self.preproc.process(data).content.articles[0].paragraphs]

        # Assert
        self.assertEqual(["hej gerne testes", "hej rumskibet Karsten testes I dag tak"], output)

    @patch('pre_processing.NJPreProcessor.call_lemmatize_api')
    def test__process__lemmatize(self, mock_post):
        # Arrange
        data = self.setup_data(["tanken er fyldt op"])
        mock_post.return_value = "tanken fyldet op"

        # Act
        output = self.preproc.process(data).content.articles[0].paragraphs[0].value

        # Assert
        self.assertEqual("tanken fyldet op", output)

    @patch('requests.post')
    def test__process__lemmatize_raise_unparseable(self, mock_post):
        # Arrange
        data = self.setup_data(["tanken er fyldt op"])
        mock_post.return_value = Exception("Test Exception")

        # Act & Assert
        with self.assertRaises(exceptions.UnparsableException) as ctx:
            self.preproc.process(data)

    @patch('requests.post')
    def test__process__lemmatize_raise_postFailed(self, mock_post):
        # Arrange
        data = self.setup_data(["tanken er fyldt op"])
        mock_post.side_effect = lambda x, y: (_ for _ in ()).throw(requests.exceptions.ConnectionError())

        # Act & Assert
        with self.assertRaises(exceptions.PostFailedException):
            self.preproc.process(data)
