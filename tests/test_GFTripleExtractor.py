import unittest
import pytest
from rdf.extractor import GFTripleExtractor

xfail = pytest.mark.xfail


class GFTripleExtractorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.te = GFTripleExtractor("./models/gf_spacy_model")

    def test__pre_process_manual(self):
        # Arrange
        self.te.pump_name = "SQ/SQE"
        data = [
            "The pump supports both oil and water.",
            "I am a sentence. I am another sentence!",
            "7 3432 734 8",
            "Awkward    spacing       is  awkward.",
            "Please refer to fig. 7"
        ]
        expected = [
            "SQ/SQE supports both oil and water.\n",
            "I am a sentence.\nI am another sentence!\n",
            "\n",
            "Awkward spacing is awkward.\n",
            "Please refer to fig. 7\n"
        ]
        actual = []

        # Act
        for test in data:
            actual.append(self.te._pre_process_manual(test))

        # Assert
        for i in range(5):
            assert expected[i] == actual[i]
