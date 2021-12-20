import re
from typing import List, Tuple

from model import Document, Article
from rdf.RdfConstants import RelationTypeConstants
from .TripleExtractor import TripleExtractor, Triple, TripleExtractorEnum
from rdf.RdfCreator import generate_uri_reference, generate_relation, generate_literal
from environment import EnvironmentVariables as Ev
Ev()


class GFTripleExtractor(TripleExtractor):
    """
    The triple extractor class specifically for Grundfos data.
    """
    def __init__(self, spacy_model, tuple_label_list=None, ignore_label_list=None) -> None:
        """

        :param spacy_model: The name/path of the spaCy model to be used as a string
        :param tuple_label_list: Not relevant
        :param ignore_label_list: Not relevant
        """
        # TODO: The pump name SHOULD NOT be hard-coded. It is only like this since we don't receive the pump name
        #  from the previous layer
        self.pump_name = "SQ/SQE"

        super().__init__(spacy_model, [], [], "http://www.KnoxGrundfos.test/")
        self._init_spacy_pipeline()

    def _init_spacy_pipeline(self):
        """
        Adds patterns for the rule-based matching of pumps.
        """
        test = Ev.instance.get_value(Ev.instance.GF_PATTERN_PATH)
        self.nlp.add_pipe("entity_ruler").from_disk(test)

    # TODO: find out if it should have common implementation in TripleExtractor
    def _append_token(self, article: Article, pair: Tuple[str, str]):
        """
        Method for creating <Manual> <mentions> and <Manual> <name> triples

        :param article: The manual to extract triples from
        :param pair: Tuple containing the name and label of the entity
        """
        # Ensure formatting of the objects name is compatible, eg. Jens Jensen -> Jens_Jensen
        object_ref, object_label = pair
        object_ref = object_ref.replace(" ", "_")
        object_label = self._convert_spacy_label_to_namespace(object_label)

        # Each entity in article added to the "Article mentions Entity" triples
        _object = generate_uri_reference(self.namespace, [object_label], object_ref)
        _subject = generate_uri_reference(self.namespace, [TripleExtractorEnum.MANUAL], article.id)
        relation = generate_relation(RelationTypeConstants.KNOX_MENTIONS)
        self.triples.append(Triple(_subject, relation, _object))
        # Each entity given the name data property
        self.triples.append(
            Triple(_object, generate_relation(RelationTypeConstants.KNOX_NAME), generate_literal(pair[0])))

    def extract_content(self, document: Document):
        """
        Calls the pre-processor, processor, and extracts the manual path for the input document.

        :param document: The document to be processed
        """
        for article in document.articles:
            # For each article, process the text and extract non-textual data in it.
            article.body = self.__pre_process_manual(article.body)
            self.__process_manual(article)
            self.__extract_manual_path(article)

    def __pre_process_manual(self, body):
        """
        Cleans the body of the manual, attempting to discard nonsensical information, as well as replacing occurrences
        of "the pump", etc. with the actual name of the pump.

        :param body: The text to be pre-processed
        :return: The cleaned text
        """
        processed_body = body
        processed_body = processed_body.replace("\n", " ")
        processed_body = processed_body.replace("- ", "")
        processed_body = processed_body.replace(". ", ".\n")
        processed_body = re.sub(r'([mM]in\.|[Ee]\.g\.|[mM]ax\.|[fF]ig(s)?\.) *\n', r'\1 ', processed_body)
        processed_body = processed_body.replace(" .", ".")
        processed_body = re.sub(r' +', ' ', processed_body)
        processed_body = re.sub(r'\d (\d |\d)+', '', processed_body)
        processed_body = processed_body.replace("\n ", "\n")
        processed_body = processed_body.replace("The pump ", self.pump_name + " ")
        processed_body = processed_body.replace(" the pump ", " " + self.pump_name + " ")
        processed_body = processed_body.replace(" the pump.", " " + self.pump_name + ".")
        processed_body = processed_body.replace("This pump ", self.pump_name + " ")
        processed_body = processed_body.replace(" this pump ", " " + self.pump_name + " ")
        processed_body = processed_body.replace(" this pump.", " " + self.pump_name + ".")
        processed_body = processed_body.replace("The pumps ", self.pump_name + " ")
        processed_body = processed_body.replace(" the pumps ", " " + self.pump_name + " ")
        processed_body = processed_body.replace(" the pumps.", " " + self.pump_name + ".")
        processed_body = processed_body.replace("These pumps ", self.pump_name + " ")
        processed_body = processed_body.replace(" these pumps ", " " + self.pump_name + " ")
        processed_body = processed_body.replace(" these pumps.", " " + self.pump_name + ".")

        # Remove short (5 chars or less), and presumably, redundant lines
        clean_processed_body = ""
        for line in processed_body.split("\n"):
            if len(line) >= 5:
                clean_processed_body += line + "\n"
            else:
                clean_processed_body += "\n"

        return clean_processed_body

    def __process_manual(self, manual: Article):
        """
        Creates pairs and calls append_token which creates triples.

        :param manual: The manual to be processed
        """
        labeled_entities = self.__process_manual_text(manual.body)

        for label_pair in labeled_entities:
            self._append_token(manual, label_pair)

    def __process_manual_text(self, body) -> List[Tuple[str, str]]:
        """
        Identifies entities in the input body, and creates entity pairs.

        :param body: The body to find entities in
        :return: The entities identified in the body
        """
        manual_entities = []
        for line in body.split("\n"):
            processed_text = self.nlp(line)

            found_pump = False

            for entity in processed_text.ents:
                if entity.label_ == "Pump":
                    found_pump = (entity.text, entity.label_)

            if found_pump:
                self.__process_pump_line(found_pump, processed_text)
            else:
                manual_entities += self.__process_non_pump_line(processed_text)

        return manual_entities

    def __process_pump_line(self, pump_pair, processed_text):
        """
        Creates triples for the PumpRelates relation.

        :param pump_pair: A Tuple containing a pump's name and label
        :param processed_text: The Doc object returned by the NLP method
        """
        pump_object_ref, pump_object_label = pump_pair
        pump_object_ref = pump_object_ref.replace(" ", "_")
        pump_object_label = self._convert_spacy_label_to_namespace(pump_object_label)
        _pump_object = generate_uri_reference(self.namespace, [pump_object_label], pump_object_ref)
        self.triples.append(
            Triple(_pump_object, generate_relation(RelationTypeConstants.KNOX_NAME), generate_literal(pump_object_ref)))

        for entity in processed_text.ents:
            if entity.label_ != "Pump":
                object_ref, object_label = entity.text, entity.label_
                object_ref = object_ref.replace(" ", "_")
                object_label = self._convert_spacy_label_to_namespace(object_label)

                # Each entity in article added to the "Article mentions Entity" triples
                _object = generate_uri_reference(self.namespace, [object_label], object_ref)
                _subject = _pump_object
                relation = generate_relation(RelationTypeConstants.KNOX_PUMP_RELATES)
                self.triples.append(Triple(_subject, relation, _object))
                # Each entity given the name data property
                self.triples.append(
                    Triple(_object, generate_relation(RelationTypeConstants.KNOX_NAME), generate_literal(entity.text)))

    def __process_non_pump_line(self, processed_text):
        """
        Identifies entities for the mentions relation.

        :param processed_text: The Doc object returned by the nlp method
        :return: A list of entities
        """
        manual_entities = []
        for entity in processed_text.ents:
            if entity.label_ not in self.ignore_label_list:
                name, label = entity.text, entity.label_
                manual_entities.append((name, label))
                self._queue_named_individual(name.replace(" ", "_"), self._convert_spacy_label_to_namespace(label))

        return manual_entities

    def __extract_manual_path(self, article: Article):
        """
        Extracts the path of the manual.

        :param article: The article whose path is to be extracted
        """
        if article.path is not None and article.path != "":
            self._append_triples_literal([TripleExtractorEnum.MANUAL], article.id,
                                         RelationTypeConstants.KNOX_LINK, article.path)
