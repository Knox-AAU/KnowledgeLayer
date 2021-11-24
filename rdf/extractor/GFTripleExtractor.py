from __future__ import annotations
import datetime
import re
from typing import List, Tuple

from model import Document, Article
from rdf.RdfConstants import RelationTypeConstants
from .TripleExtractorEnum import TripleExtractorEnum
from .TripleExtractor import TripleExtractor, Triple
from rdf.RdfCreator import generate_uri_reference, generate_relation, generate_literal
# TODO: Make a function that can determine the right preprocessor
from environment import EnvironmentVariables as Ev
import spacy
from spacy.attrs import ORTH
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
        self._init_spacy()

    def _init_spacy(self):
        """
        Loads the custom spaCy pipeline, adds special cases for the tokenizer, and adds patterns for the
        rule-based matching of pumps.
        """
        pumps = self.__extract_pumps_from_patterns()

        # Add special rules to tokenizer for each pump name
        for pump in pumps:
            self.nlp.tokenizer.add_special_case(pump, [{ORTH: pump}])

        # Load rule-based matching and its patterns specified in the .env
        self.nlp.add_pipe("entity_ruler").from_disk(Ev.instance.get_value(Ev.instance.GF_PATTERN_PATH))

    def __extract_pumps_from_patterns(self) -> List[str]:
        """
        Extracts all pump names from the file containing a list of Grundfos pumps.
        :return: List of pump names
        """
        pump_names = []

        pump_file_path = Ev.instance.get_value(Ev.instance.GF_PATTERN_PATH)

        pump_pattern = re.compile(r'"pattern": "(.*)"')

        with open(pump_file_path, "r") as pump_file:
            for line in pump_file:
                pump_names.append(pump_pattern.search(line).group(1))

        return pump_names

    # TODO: find out if it should have common implementation in TripleExtractor
    def _append_token(self, article: Article, pair: Tuple[str, str]):
        # Ensure formatting of the objects name is compatible, eg. Jens Jensen -> Jens_Jensen
        object_ref, object_label = pair
        object_ref = object_ref.replace(" ", "_")
        object_label = self._convert_spacy_label_to_namespace(object_label)

        # Each entity in article added to the "Article mentions Entity" triples
        _object = generate_uri_reference(self.namespace, [object_label], object_ref)
        _subject = generate_uri_reference(self.namespace, [TripleExtractorEnum.PUMP], article.id)
        relation = generate_relation(RelationTypeConstants.KNOX_MENTIONS)
        self.triples.append(Triple(_subject, relation, _object))
        # Each entity given the name data property
        self.triples.append(
            Triple(_object, generate_relation(RelationTypeConstants.KNOX_NAME), generate_literal(pair[0])))

    def extract_content(self, document: Document):
        for article in document.articles:
            # For each article, process the text and extract non-textual data in it.
            self.__process_manual(article)
            self.__extract_manual_path(article)

    def __process_manual(self, manual: Article):
        labeled_entities = self.__process_manual_text(manual.body)

        # TODO: maybe some check whether it is related to pump or is just mentioned in the manual
        for label_pair in labeled_entities:
            self._append_token(manual, label_pair)

    def __process_manual_text(self, body) -> List[(str, str)]:

        # TODO: maybe do text preprocessing here
        processed_text = self.nlp(body)

        manual_entities = []

        for entity in processed_text.ents:
            if entity.label_ not in self.ignore_label_list:
                name, label = entity.text, entity.label_

                manual_entities.append((name, label))
                self._queue_named_individual(name.replace(" ", "_"), self._convert_spacy_label_to_namespace(label))

        return manual_entities

    def __extract_manual_path(self, article: Article):
        if article.path is not None and article.path != "":
            self._append_triples_literal([TripleExtractorEnum.MANUAL], article.id,
                                         RelationTypeConstants.KNOX_LINK, article.path)