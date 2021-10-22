from doc_classification import Document
from word_count.TermFrequency import *
from typing import List
# from knox_util import print
import json
from json import JSONEncoder
from environment.EnvironmentConstants import EnvironmentVariables as Ev
# import re


class WordFrequencyHandler:
    """
    Class wrapper for the word frequency count module produced by Group-D in the knox project
    """

    def __init__(self) -> None:
        self.tf = TermFrequency()
        self.back_up_file_prefix = 'word_count_'
        self.word_frequencies_ready_for_sending = []

    def word_count_document(self, document : Document) -> None:
        """
        Entry point for running word counting on a string og text

        :param document_title: The title of the article the word counting is done for
        :param article_content: The content of the article to do word counting
        :param extracted_from_list: A list of strings containing the file names the article was extracted from
        """
        # article_content = re.sub(r'\d+\s*', '', article_content)
        # article_content = re.sub(r'[.,\-\/:;!"\\@?\'¨~^#%&()<>[\]{}]','',article_content)

        # Process the article text
        self.tf.process(document.title, document.body)

        # Convert the word counting data into a class instance representing the JSON
        self.__convert_to_word_frequency_JSON_object__(document)
        # Reset the handler to make it ready for the next article
        self.__reset__()

    def __concatenate_extracted_from__(self, path_list: List) -> str:
        """
        Concatenate all the file names that an article has been extracted from into a single comma seperated string.

        :param path_list: A list of path names
        :return: A comma seperated string of the path names from the input
        """
        ret_val: str = ''

        count_extracted_from_paths = len(path_list)
        current_count = 1
        for path in path_list:
            ret_val += path

            if count_extracted_from_paths > current_count:
                ret_val += ','
            current_count += 1

        return ret_val

    def __convert_to_word_frequency_JSON_object__(self, document: Document) -> None:
        """
        Converts the word counting data into an class instance for sending to the Data layer.

        :param title: The title of the article that had word frequency done
        :param extracted_from: A single comma seperated string of the path names the article was extracted from
        """
        frequency_data = self.tf[document.title]
        total_words = self.tf[document.title].length
        frequency_object = __WordFrequency__(document.title, document.paths, frequency_data, total_words, document.publisher)

        if frequency_object.articletitle == '':
            print('Found empty title. Skipping', 'debug')
            return

        json_object = json.dumps(frequency_object, cls=__WordFrequencyEncoder__, sort_keys=True, indent=4,
                                 ensure_ascii=False)

        # TODO: Find a better way to array-ify the JSON
        self.word_frequencies_ready_for_sending.append("[" + json_object + "]")

    def __reset__(self, hard_reset=False):
        """
        Resets the WordFrequencyHandler to ready it for processing the next article.

        :param hard_reset: Indicates whether a hard reset of the handler should be done, removing all pending word counts not sent yet (default: False)
        """
        self.tf = TermFrequency()
        if hard_reset:
            self.word_frequencies_ready_for_sending = []

    def get_next_pending_wordcount(self):
        """
        Returns the next pending word count
        :return: The next pending word count
        """
        return self.word_frequencies_ready_for_sending.pop()


class __WordFrequency__:
    """
    Parent wrapper class holding the word count data transformed into JSON
    """

    def __init__(self, title: str, extracted_from: str, frequency_data: List, total_words: int, publication: str) -> None:
        self.words: List = []
        for word in frequency_data:
            if word == '':
                print('Found empty word, skipping...', 'debug')
                continue

            count = frequency_data[word]
            self.words.append(Word(word, count))

        self.articletitle: str = title
        self.filepath: str = extracted_from
        self.totalwordsinarticle = total_words
        self.publication = publication


class Word:
    """
    Wrapper class for a single word in the word count data
    """

    def __init__(self, word: str, word_count: int) -> None:
        self.word = word
        self.amount = word_count


class __WordFrequencyEncoder__(JSONEncoder):
    """
    Custom JSONEncoder for translating the __WordFrequency__ class instance into JSON
    """

    def default(self, o) -> None:
        return o.__dict__
