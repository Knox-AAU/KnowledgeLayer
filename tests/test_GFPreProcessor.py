from typing import List
import pytest
from unittest.mock import patch
import unittest
from model.Document import Document, Article
from pre_processing import GFPreProcessor

xfail = pytest.mark.xfail


class GFPreProcessorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.preproc = GFPreProcessor()

    def create_article(self, title: str, body: str) -> Article:
        return Article(title, body, "/testpath.extension")

    def setup_data(self, articleBodies: List[str]) -> Document:
        makeArticle = lambda title, body: Article(title, body, "/testpath.extension")
        document = Document("Test Publisher")
        document.articles = [makeArticle(f'TestTitle Nr. {i}', v) for i, v in enumerate(articleBodies)]
        return document

    def test__to_lower(self):
        # Arrange
        data = [
            "I am a Sentence with UpperCase LettErs!",
            "I too have uppercase letters",
            "Actually THE LAST sentence only HAD 1",
            "I'm running OUT oF eXaMpLeS...",
            "here's a last one"
        ]
        expected = [
            "i am a sentence with uppercase letters!",
            "i too have uppercase letters",
            "actually the last sentence only had 1",
            "i'm running out of examples...",
            "here's a last one"
        ]
        actual = []

        # Act
        for test in data:
            actual.append(self.preproc.to_lower(test))

        # Assert
        assert actual[0] == expected[0]
        assert actual[1] == expected[1]
        assert actual[2] == expected[2]
        assert actual[3] == expected[3]
        assert actual[4] == expected[4]

    def test__remove_special_characters(self):
        # Arrange
        data = [
            "I'm working @home today.",
            "Grundfos: The Test Data of a #Lifetime!",
            "They owe me $10 million, though.",
            "Are we finished testing now?",
            "I am different"
        ]
        expected = [
            "Im working home today",
            "Grundfos The Test Data of a Lifetime",
            "They owe me 10 million though",
            "Are we finished testing now",
            "I am different"
        ]
        actual = []

        # Act
        for test in data:
            actual.append(self.preproc.remove_special_characters(test))

        # Assert
        assert actual[0] == expected[0]
        assert actual[1] == expected[1]
        assert actual[2] == expected[2]
        assert actual[3] == expected[3]
        assert actual[4] == expected[4]

    def test__numbers_to_text(self):
        # Arrange
        data = [
            "Time 4 some numb3rs!",
            "I could do this 55 times without issue",
            "The secret code is: 953810",
            "You better give me 100% today!",
            "Who needs numbers, anyway?"
        ]
        expected = [
            "Time four some numbthreers!",
            "I could do this five_five times without issue",
            "The secret code is: nine_five_three_eight_one_zero",
            "You better give me one_zero_zero% today!",
            "Who needs numbers, anyway?"
        ]
        actual = []

        # Act
        for test in data:
            actual.append(self.preproc.numbers_to_text(test))

        # Assert
        assert actual[0] == expected[0]
        assert actual[1] == expected[1]
        assert actual[2] == expected[2]
        assert actual[3] == expected[3]
        assert actual[4] == expected[4]

    @patch('pre_processing.PreProcessor.lemmatize')
    def test__process_text(self, mock_post):
        # Arrange
        data = self.setup_data(["50 % glycol at 20 °C means a viscosity of approx. 10 mm2/s (10 cSt) and a reduction of the pump performance by approx. 15 %."])
        mock_post.return_value = "five_zero  glycol at two_zero C mean a viscosity of approx one_zero mmtwos one_zero cSt and a reduction of the pump performance by approx one_five "
        expected = "five_zero  glycol at two_zero c mean a viscosity of approx one_zero mmtwos one_zero cst and a reduction of the pump performance by approx one_five "

        # Act
        actual = self.preproc.__process_text__(data, data.articles[0].body)

        # Assert
        self.assertEqual(expected, actual)

    @patch('pre_processing.PreProcessor.lemmatize')
    def test__process(self, mock_post):
        # Arrange
        data = self.setup_data(["-20 °C to 70 °C (-4 °F to 158 °F) (factory-filled with anti-freeze liquid)."])
        mock_post.return_value = "two_zero c to seven_zero c four f to one_five_eight F factoryfille with antifreeze liquid"

        article = Article("TestTitle Nr. 0", "two_zero c to seven_zero c four f to one_five_eight f factoryfille with antifreeze liquid", "/testpath.extension")
        expected = Document("Test Publisher", "", [article])

        # Act
        actual = self.preproc.process(data)

        # Assert
        assert expected.articles[0].body == actual.articles[0].body
