from __future__ import annotations
import datetime
from typing import List, OrderedDict, Any, Tuple, NamedTuple

import spacy

from model import Document, Article
from rdf.RdfConstants import RelationTypeConstants
from rdf.RdfCreator import generate_uri_reference, generate_relation, generate_literal, store_rdf_triples
from .TripleExtractorEnum import TripleExtractorEnum
# TODO: Make a function that can determine the right preprocessor
from environment import EnvironmentVariables as Ev
import spacy
Ev()


class GFTripleExtractor(TripleExtractor):
    # nlp: OrderedDict = None
    def __init__(self, spacy_model, tuple_label_list=None, ignore_label_list=None) -> None:
        # PreProcessor.nlp = self.nlp
        self.nlp = spacy.load(spacy_model)
        self.namespace = Ev.instance.get_value(Ev.instance.ONTOLOGY_NAMESPACE)
        self.triples = []
        self.named_individual = []
        if tuple_label_list is None:
            # TODO: Give our labels
            labels = [["PER", "Person"], ["ORG", "Organisation"], ["LOC", "Location"], ["DATE", "Date"],
                      ["NORP", "Norp"]]
            self.tuple_label_list = [{'spacy_label': v[0], 'namespace': v[1]} for v in labels]
        else:
            self.tuple_label_list = tuple_label_list

        # TODO: Find out if we need this
        if ignore_label_list is None:
            self.ignore_label_list = ["MISC"]
        else:
            self.ignore_label_list = ignore_label_list

    def process_publication(self, document: Document) -> List[Triple]:
        """
        Input:
            publication: Publication - A Publication class which is the content of a newspaper
            file_path : str - File path to the publication being processed

        Writes entity triples to file
        """
        # Extract publication info and adds it to the RDF triples.
        self.extract_publication(document)

        for article in document.articles:
            # For each article, process the text and extract non-textual data in it.
            self.__process_article(article)
            self.__extract_article(article, document)

        # Adds named individuals to the triples list.
        self.__append_named_individual()

        # Function from rdf.RdfCreator, writes triples to file
        store_rdf_triples(self.triples)

        return self.triples

    def __queue_named_individual(self, prop_1, prop_2) -> None:
        """
        Adds the named individuals to the named_individual list if it's not already in it.
        """
        if [prop_1, prop_2] not in self.named_individual:
            self.named_individual.append([prop_1, prop_2])

    def extract_publication(self, document: Document) -> None:
        if document.publication is not None:
            
            # Formatted name of a publisher and publication
            publication_formatted = document.publication.replace(" ", "_")
            publisher_formatted = document.publisher.replace(" ", "_")

            # Adds publication as a named individual
            self.__queue_named_individual(publication_formatted, TripleExtractorEnum.PUBLICATION)
            # Add publication name as data property
            self.__append_triples_literal([TripleExtractorEnum.PUBLICATION], publication_formatted,
                                          RelationTypeConstants.KNOX_NAME, document.publication)

            # Add publisher name as data property
            self.__append_triples_literal([TripleExtractorEnum.PUBLISHER], publisher_formatted,
                                          RelationTypeConstants.KNOX_NAME, publisher_formatted)
            # Add the "Publisher publishes Publication" relation
            self.__append_triples_uri([TripleExtractorEnum.PUBLISHER], publisher_formatted,
                                      [TripleExtractorEnum.PUBLICATION], publication_formatted,
                                      RelationTypeConstants.KNOX_PUBLISHES)

    def __convert_spacy_label_to_namespace(self, string: str) -> str:
        """
        Input:
            string: str - A string matching a spacy label
        Returns:
            A string matching a class in the ontology.
        """
        for label in self.tuple_label_list:
            # Assumes that tuple_label_list is a list of dicts with the format: {"spacy_label": xxx, "target_label": xxx}
            if string == str(label['spacy_label']):
                # return the chosen name for the spaCy label
                return str(label['namespace'])
        else:
            return string

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

    def __append_token(self, article: Article, pair: Tuple[str, str]):
        # Ensure formatting of the objects name is compatible, eg. Jens Jensen -> Jens_Jensen
        object_ref, object_label = pair
        object_ref = object_ref.replace(" ", "_")
        object_label = self.__convert_spacy_label_to_namespace(object_label)

        # Each entity in article added to the "Article mentions Entity" triples
        _object = generate_uri_reference(self.namespace, [object_label], object_ref)
        _subject = generate_uri_reference(self.namespace, [TripleExtractorEnum.ARTICLE], article.id)
        relation = generate_relation(RelationTypeConstants.KNOX_MENTIONS)
        self.triples.append(Triple(_subject, relation, _object))
        # Each entity given the name data property
        self.triples.append(
            Triple(_object, generate_relation(RelationTypeConstants.KNOX_NAME), generate_literal(pair[0])))

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

    def __append_triples_literal(self, uri_types: List[str], uri_value: Any, relation_type: str, literal: str):
        self.triples.append(Triple(
            generate_uri_reference(self.namespace, uri_types, uri_value),
            generate_relation(relation_type),
            generate_literal(literal)
        ))

    def __append_triples_uri(self, uri_types1: List[str], uri_value1: Any,
                             uri_types2: List[str], uri_value2: Any, relation_type: str):
        self.triples.append(Triple(
            generate_uri_reference(self.namespace, uri_types1, uri_value1),
            generate_relation(relation_type),
            generate_uri_reference(self.namespace, uri_types2, uri_value2),
        ))

    def __append_named_individual(self) -> None:
        """
        Appends each named individual to the triples list.
        """

        # prop1 = The specific location/person/organisation or so on
        # prop2 = The type of Knox:Class prop1 is a member of.
        for prop1, prop2 in self.named_individual:
            self.triples.append(Triple(
                generate_uri_reference(self.namespace, [prop2], prop1),
                generate_relation(RelationTypeConstants.RDF_TYPE),
                generate_relation(RelationTypeConstants.OWL_NAMED_INDIVIDUAL)
            ))

            self.triples.append(Triple(
                generate_uri_reference(self.namespace, [prop2], prop1),
                generate_relation(RelationTypeConstants.RDF_TYPE),
                generate_uri_reference(self.namespace, ref=prop2)
            ))


class Triple(NamedTuple):
    subject: str
    relation: str
    object: str
