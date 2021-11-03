import decimal
from typing import Optional, List, Any
import numpy as np

import spacy
from spacy.lang.da.stop_words import STOP_WORDS


class PublicationGenerator:
    def __init__(self, data_classification: str, repeat_amount: int = 1, article_amount: int = 1, paragraph_amount: int = 1,
                 paragraph_word_count: int = 200, stop_word_density: decimal = 0, seed: Optional[int] = None):
        self.stop_word_density = stop_word_density
        self.article_amount = article_amount
        self.paragraph_word_count = paragraph_word_count
        self.paragraph_amount = paragraph_amount
        self.repeat_amount = repeat_amount
        self.data_classification = data_classification
        self.spacy_model = spacy.load("da_core_news_lg")
        self.seed = seed
        self.__randomState = np.random.RandomState()

    def publication_generator(self):
        for i in range(self.repeat_amount):
            yield self.__generate_new_publication()

    def set_seed(self, seed: Optional[int]):
        self.__randomState = np.random.RandomState(seed=seed)

    def __generate_new_publication(self) -> dict:
        if self.data_classification == "NJ":
            return self.__generate_NJ_publication()
        elif self.data_classification == "GF":
            return self.__generate_GF_publication()
        else:
            raise AttributeError(f'ERROR: Cannot generate data for \'{self.data_classification}\'.')

    def __generate_NJ_publication(self) -> dict:
        articles = [self.__generate_article() for _ in range(self.article_amount)]
        return dict(__class__="Wrapper", __module__="knox_source_data_io.models.wrapper", type="Publication",
                    schema="TestSchema",
                    generator=dict(app="This App", version="0.0.0.1", generated_at="Some time ago"),
                    content=dict(__class__="Publication", __module__="knox_source_data_io.models.publication",
                                 publication="Publication1", published_at="2018-03-27T00:00:00+02:00",
                                 publisher="NordJyskePublisher", pages=3, articles=articles))

    def __generate_GF_publication(self) -> dict:
        pass

    def __generate_article(self) -> dict:
        paragraphs = [self.__generate_paragraph() for _ in range(self.paragraph_amount)]
        return dict(__class__="Article", __module__="knox_source_data_io.models.publication",
                    headline="This is a test headline", id=0, extracted_from=["/testpath"], paragraphs=paragraphs)

    def __generate_paragraph(self) -> dict:
        content = self.__get_random_sentence()
        self.__insert_stop_words(content)
        value = self.__join_content(content)
        return dict(__class__="Paragraph", __module__="knox_source_data_io.models.publication",
                    kind="Test Kind", value=value)

    def __get_random_sentence(self):
        vocab = list(self.spacy_model.vocab.strings)
        vocab_length = len(vocab)

        content = [self.__get_random_entry(vocab, vocab_length)
                   for _ in range(self.paragraph_word_count)]
        return content

    def __join_content(self, content):
        join_list = [' ', ' .', ', ', '-']
        value = ''
        for i in range(len(content)):
            value = value + self.__get_random_entry(join_list) + content[i]
        return value

    def __insert_stop_words(self, content: List[str]) -> None:
        stop_words = list(STOP_WORDS)
        stop_word_length = len(stop_words)
        stop_word_count = int(self.paragraph_word_count * self.stop_word_density)
        hits = self.__randomState.choice(len(content), stop_word_count, replace=False)
        for hit in hits:
            content[hit] = self.__get_random_entry(stop_words, stop_word_length)

    def __get_random_entry(self, entry_list: List[Any], max_index: Optional[int] = None) -> str:
        if max_index is None:
            max_index = len(entry_list)
        rand_index = self.__randomState.randint(max_index)
        return entry_list[rand_index]
