import unittest
from unittest.mock import patch
from rdf import NJTripleExtractor
from model import Document, Article, Byline
import spacy
from environment import EnvironmentVariables as Ev
from typing import List
from rdf.extractor import Triple
from utils import load_model

Ev()

def generate_document() -> Document:
    articles = [Article(title="ArticleTest",
                        body="For at give et eksempel på hvad social ulighed i sundhed egentligt kan betyde, vil vi ved hjælp af data fra Sundhedsstyrelsen og de to eksperter gennemgå en række udvalgte faktorer med to fiktive kvinder. En højtuddannet kvinde og en kvinde, der udelukkende har færdiggjort folkeskolen." +
                             "Begge kvinder er 30 år, og vi kalder dem henholdsvis for Tinna og Alice. Tinna er ufaglært lagermedarbejder, og Alice er uddannet jurist. Dermed er der også forskel i kvindernes indkomst, hvor Alice tjener mere end Tinna.",
                        path="/this/is/test/path", article_id="1")]
    document = Document(publisher="Test", publication="Test", articles=articles, date="01-01-2020")

    return document

class TripleExtractorTests(unittest.TestCase):



    # Does it correctly identify triples?
    # Does it correctly work with wrong input (or something)
    # ------- Non strings replacing strings
    # Does it run without failing on a correct input?
    # Does it run equally well with and without required fields?
    # --------------------------------------------------------------
    # Does an empty body of text crash it?
    # Does any empty (but required) fields crash it?
    # If there are no articles, what happens?
    # Are the correct functions being called?
    # Are labels correctly converted and are ignored labels NOT included?

    @classmethod
    def setUpClass(cls) -> None:
        spacy_model = Ev.instance.get_value(Ev.instance.NJ_SPACY_MODEL)
        cls.spacy_model = load_model(spacy_model)
        cls.triple_extractor = NJTripleExtractor(spacy_model)

    @patch('requests.post')
    def test_process_publication__one_article__list_of_triples(self, mock_post):
        # Arrange
        mock_post.return_value = True
        articles = [Article(title="ArticleTest",
                            body="For at give et eksempel på hvad social ulighed i sundhed egentligt kan betyde, vil vi ved hjælp af data fra Sundhedsstyrelsen og de to eksperter gennemgå en række udvalgte faktorer med to fiktive kvinder. En højtuddannet kvinde og en kvinde, der udelukkende har færdiggjort folkeskolen." +
                                 "Begge kvinder er 30 år, og vi kalder dem henholdsvis for Tinna og Alice. Tinna er ufaglært lagermedarbejder, og Alice er uddannet jurist. Dermed er der også forskel i kvindernes indkomst, hvor Alice tjener mere end Tinna.",
                            path="/this/is/test/path", article_id="1")]
        document = Document(publisher="Test", publication="Test", articles=articles, date="2021-07-27")
        # Act
        result = self.triple_extractor.process_publication(document=document)
        # Assert
        is_of_type_triple = [isinstance(v, Triple) for v in result]
        self.assertTrue(all(is_of_type_triple))

    @patch('requests.post')
    def test_process_publication__multiple_article__list_of_triples(self, mock_post):
        # Arrange
        mock_post.return_value = True
        articles = 20 * [Article(title="ArticleTest",
                            body="For at give et eksempel på hvad social ulighed i sundhed egentligt kan betyde, vil vi ved hjælp af data fra Sundhedsstyrelsen og de to eksperter gennemgå en række udvalgte faktorer med to fiktive kvinder. En højtuddannet kvinde og en kvinde, der udelukkende har færdiggjort folkeskolen." +
                                 "Begge kvinder er 30 år, og vi kalder dem henholdsvis for Tinna og Alice. Tinna er ufaglært lagermedarbejder, og Alice er uddannet jurist. Dermed er der også forskel i kvindernes indkomst, hvor Alice tjener mere end Tinna.",
                            path="/this/is/test/path", article_id="1")]
        document = Document(publisher="Test", publication="Test", articles=articles, date="2021-07-27")
        # Act
        result = self.triple_extractor.process_publication(document=document)
        # Assert
        is_of_type_triple = [isinstance(v, Triple) for v in result]
        self.assertTrue(all(is_of_type_triple))

    @patch('requests.post')
    def test_process_publication__publication_as_integer__error_thrown(self, mock_post):
        # Arrange
        mock_post.return_value = True
        articles = [Article(title="ArticleTest",
                            body="For at give et eksempel på hvad social ulighed i sundhed egentligt kan betyde, vil vi ved hjælp af data fra Sundhedsstyrelsen og de to eksperter gennemgå en række udvalgte faktorer med to fiktive kvinder. En højtuddannet kvinde og en kvinde, der udelukkende har færdiggjort folkeskolen." +
                                 "Begge kvinder er 30 år, og vi kalder dem henholdsvis for Tinna og Alice. Tinna er ufaglært lagermedarbejder, og Alice er uddannet jurist. Dermed er der også forskel i kvindernes indkomst, hvor Alice tjener mere end Tinna.",
                            path="/this/is/test/path", article_id="1")]
        document = Document(publisher="Test", publication=123, articles=articles, date="2021-07-27")
        # Act
        result = lambda: self.triple_extractor.process_publication(document=document)
        # Assert
        self.assertRaises(AttributeError, result)


    @patch('requests.post')
    def test_process_publication__body_invalid_character__no_error_thrown(self, mock_post):
        # Arrange
        mock_post.return_value = True
        articles = [Article(title="ArticleTest",
                            body="For — переменная + 變量 + ตัวแปร",
                            path="/this/is/test/path", article_id="1")]
        document = Document(publisher="Test", publication="Test", articles=articles, date="2021-07-27")
        # Act
        result = self.triple_extractor.process_publication(document=document)
        # Assert
        is_of_type_triple = [isinstance(v, Triple) for v in result]
        self.assertTrue(all(is_of_type_triple))


    @patch('requests.post')
    def test_process_publication__non_required_fields_missing__list_of_triples(self, mock_post):
        # Arrange
        mock_post.return_value = True
        byline = Byline(name="Carlo, Harlo")
        articles = [Article(title="ArticleTest",
                            body="For at give et eksempel på hvad social ulighed i sundhed egentligt kan betyde, vil vi ved hjælp af data fra Sundhedsstyrelsen og de to eksperter gennemgå en række udvalgte faktorer med to fiktive kvinder. En højtuddannet kvinde og en kvinde, der udelukkende har færdiggjort folkeskolen." +
                                 "Begge kvinder er 30 år, og vi kalder dem henholdsvis for Tinna og Alice. Tinna er ufaglært lagermedarbejder, og Alice er uddannet jurist. Dermed er der også forskel i kvindernes indkomst, hvor Alice tjener mere end Tinna.",
                            path="/this/is/test/path", byline=byline)]
        document = Document(publisher="Test", publication=None, articles=articles, date=None)
        # Act
        result = self.triple_extractor.process_publication(document=document)
        # Assert
        is_of_type_triple = [isinstance(v, Triple) for v in result]
        self.assertTrue(all(is_of_type_triple))


    @patch('requests.post')
    def test_process_publication__non_required_fields_present__list_of_triples(self, mock_post):
        # Arrange
        mock_post.return_value = True
        byline = Byline(name="Carlo, Harlo", email="presidentoftesting@knox.dk")
        articles = [Article(title="ArticleTest",
                            body="For at give et eksempel på hvad social ulighed i sundhed egentligt kan betyde, vil vi ved hjælp af data fra Sundhedsstyrelsen og de to eksperter gennemgå en række udvalgte faktorer med to fiktive kvinder. En højtuddannet kvinde og en kvinde, der udelukkende har færdiggjort folkeskolen." +
                                 "Begge kvinder er 30 år, og vi kalder dem henholdsvis for Tinna og Alice. Tinna er ufaglært lagermedarbejder, og Alice er uddannet jurist. Dermed er der også forskel i kvindernes indkomst, hvor Alice tjener mere end Tinna.",
                            path="/this/is/test/path", article_id="1", byline=byline)]
        document = Document(publisher="Test", publication="Test", articles=articles, date="2021-07-27")
        # Act
        result = self.triple_extractor.process_publication(document=document)
        # Assert
        is_of_type_triple = [isinstance(v, Triple) for v in result]
        self.assertTrue(all(is_of_type_triple))

    @patch('requests.post')
    def test_process_publication__send_empty_article__list_of_triples(self, mock_post):
        #Arrange
        mock_post.return_value = True
        document = Document(publisher="Test", publication="Test", articles=[], date="2021-07-27")

        #Act
        triples = self.triple_extractor.process_publication(document)
        is_of_type_triple = [isinstance(v, Triple) for v in triples]

        #Assert
        self.assertTrue(all(is_of_type_triple))
    from rdf.RdfCreator import store_rdf_triples
    @patch('requests.post')
    def test_process_publication__send_empty_publisher__no_error_thrown(self, mock_post):
        # Arrange
        mock_post.return_value = True
        document = Document(publisher="", publication="Test", articles=[], date="2021-07-27")

        # Act
        triples = self.triple_extractor.process_publication(document)
        publisher_relations = [triple for triple in triples if triple.relation == 'knox:publishes']
        is_empty = len(publisher_relations) == 0

        # Assert
        self.assertTrue(is_empty)


if __name__ == '__main__':
    unittest.main()
