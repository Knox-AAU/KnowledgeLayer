import pytest
from unittest.mock import patch
import unittest
from doc_classification import DocumentClassifier
from tests.json_test_data import *

xfail = pytest.mark.xfail


class DocumentClassifierTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.classifier = DocumentClassifier()

    @patch('pre_processing.PreProcessor.lemmatize')
    def test__classify_json_gf(self, mock):
        # Arrange
        json_input = classifier_gf_json
        mock.return_value = "I be a Grundfos paragraph twond paragraph"
        expected = [
            "Grundfos A/S",
            "i be a grundfos paragraph twond paragraph",
            "/srv/data/grundfosarchive_few_files/Grundfosliterature-6253430.pdf"
        ]

        # Act
        actual = self.classifier.classify(json_input)
        publisher = actual.publisher
        body = actual.articles[0].body
        path = actual.articles[0].path

        # Assert
        assert publisher == expected[0]
        assert body == expected[1]
        assert path == expected[2]
