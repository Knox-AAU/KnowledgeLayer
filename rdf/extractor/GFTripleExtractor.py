from __future__ import annotations
import datetime
from typing import List, OrderedDict, Any, Tuple, NamedTuple

import spacy

from model import Document, Article
from rdf.RdfConstants import RelationTypeConstants
from rdf.RdfCreator import generate_uri_reference, generate_relation, generate_literal, store_rdf_triples
from .TripleExtractorEnum import TripleExtractorEnum
from .TripleExtractor import TripleExtractor, Triple
# TODO: Make a function that can determine the right preprocessor
from environment import EnvironmentVariables as Ev
import spacy
Ev()


class GFTripleExtractor(TripleExtractor):
    def __init__(self, spacy_model, tuple_label_list=None, ignore_label_list=None) -> None:
        if tuple_label_list is None:
            labels = [["PER", "Person"], ["ORG", "Organisation"], ["LOC", "Location"], ["DATE", "Date"],
                      ["NORP", "Norp"]] # TODO: write the grundfos labels
            self.tuple_label_list = [{'spacy_label': v[0], 'namespace': v[1]} for v in labels]

        if ignore_label_list is None:
            ignore_label_list = ["MISC"]

        super().__init__(spacy_model, tuple_label_list, ignore_label_list, "Grundfos")

    def __process_article_text(self, article_text: str) -> List[(str, str)]:
        """
        Input:
            article_text: str - The entire content of an article
        Returns:
            A list of "string" and label pairs. Eg: [("Jens Jensen", Person), ...]

        Runs the article text through the spacy pipeline
        """
        # Perform NLP on the article text, with the purpose of doing a NER
        document = self.nlp(article_text)

        # Create article entity from the document entities
        article_entities = []

        for entities in document.ents:
            name = entities.text
            # label_ is correct for acquiring the spaCy string version of the entity
            label = entities.label_

            # ignore ignored labels, expects ignore_label_list to be a list of strings
            if label not in self.ignore_label_list:
                # Add entity to list, create it as named individual.
                article_entities.append((name, label))
                self.__queue_named_individual(name.replace(" ", "_"), self.__convert_spacy_label_to_namespace(label))
        return article_entities

    def __process_article(self, article: Article) -> None:
        """
        Input:
            article: Article - An Article object from the loader package
        Returns: None
        """

        # Article text is split into multiple paragraph objects in the Json, this is joined into one string.
        ##content = ' '.join(para.value for para in article.paragraphs).replace('”', '"')

        # Does nlp on the text
        article_entities = self.__process_article_text(article.body)

        for pair in article_entities:
            self.__append_token(article, pair)

    def __extract_article(self, article: Article, document: Document) -> None:
        """
        Input:
            article: Article - An instance of the article from input file
            publication: Publication - The publication object holding information about a publication

        Creates triple based on data received through the input file
        """
        # article_id = str(article.id)
        self.__extract_article_meta(article, document)
        self.__extract_article_byline(article)
        self.__extract_article_path(article)

    def __extract_article_path(self, article: Article):
        # For each file that an article is extracted from, add it to the article as a data property
        # if len(article.extracted_from) > 0:
        #     for ocr_file in article.extracted_from:
        if article.path is not None and article.path != "":
            self.__append_triples_literal([TripleExtractorEnum.ARTICLE], article.id,
                                          RelationTypeConstants.KNOX_LINK, article.path)

    def __extract_article_byline(self, article: Article):
        # If the byline exists add the author name to the RDF triples. Author name is required if byline exists.
        byline = article.byline
        if byline is not None:
            # article.byline.name stores the author of the article's name, hence author_name
            author_name = byline.name.replace(" ", "_")

            self.__append_triples_literal([TripleExtractorEnum.AUTHOR], author_name,
                                          RelationTypeConstants.KNOX_NAME, byline.name)
            # Creates the author as a named individual
            self.__queue_named_individual(author_name, TripleExtractorEnum.AUTHOR)
            # Adds the Article isWrittenBy Author relation to the triples list
            self.__append_triples_uri([TripleExtractorEnum.ARTICLE], article.id, [TripleExtractorEnum.AUTHOR],
                                      author_name, RelationTypeConstants.KNOX_IS_WRITTEN_BY)
            # Since email is not required in the byline, if it exists: add the authors email as a data property to the author.
            if byline.email is not None:
                self.__append_triples_literal([TripleExtractorEnum.AUTHOR], author_name,
                                              RelationTypeConstants.KNOX_EMAIL, byline.email)

    def __extract_article_meta(self, article: Article, document: Document):

        # Creates the article as a named individual
        self.__queue_named_individual(article.id, TripleExtractorEnum.ARTICLE)

        # Adds the Article knox:Article_Title Title data to the turtle output
        self.__append_triples_literal([TripleExtractorEnum.ARTICLE], article.id,
                                      RelationTypeConstants.KNOX_ARTICLE_TITLE, article.title)

        publisher = document.publisher.replace(" ", "_")
        # Creates the publisher as a named individual
        self.__queue_named_individual(publisher, TripleExtractorEnum.PUBLISHER)
        # Adds the Article isPublishedBy Publication relation to the turtle output
        self.__append_triples_uri([TripleExtractorEnum.ARTICLE], article.id, [TripleExtractorEnum.PUBLISHER],
                                  publisher, RelationTypeConstants.KNOX_IS_PUBLISHED_BY)

        # Adds the publication date to the article, if it exists.
        if document.date is not None:
            date = datetime.date.fromisoformat(document.date)
            self.__append_triples_literal([TripleExtractorEnum.ARTICLE], article.id,
                                          RelationTypeConstants.KNOX_PUBLICATION_DAY, str(date.day))
            self.__append_triples_literal([TripleExtractorEnum.ARTICLE], article.id,
                                          RelationTypeConstants.KNOX_PUBLICATION_MONTH, str(date.month))
            self.__append_triples_literal([TripleExtractorEnum.ARTICLE], article.id,
                                          RelationTypeConstants.KNOX_PUBLICATION_YEAR, str(date.year))
