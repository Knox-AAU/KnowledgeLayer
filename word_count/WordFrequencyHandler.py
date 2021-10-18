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

    def word_count_document(self, document_title: str, article_content: str, extracted_from_list: List) -> None:
        """
        Inputs:
            document_title: str - The title of the article the word counting is done for
            article_content: str - The content of the article to do word counting
            extracted_from_list: list - A list of strings containing the file names the article was extracted from

        Entry point for running word counting on a string og text
        """
        # article_content = re.sub(r'\d+\s*', '', article_content)
        # article_content = re.sub(r'[.,\-\/:;!"\\@?\'¨~^#%&()<>[\]{}]','',article_content)

        # Process the article text
        self.tf.process(document_title, article_content)

        # Create extracted from string
        extracted_from: str = self.__concatenate_extracted_from__(extracted_from_list)

        # Convert the word counting data into a class instance representing the JSON
        self.__convert_to_word_frequency_JSON_object__(document_title, extracted_from)
        # Reset the handler to make it ready for the next article
        self.__reset__()

    def __concatenate_extracted_from__(self, path_list: List) -> str:
        """
        Inputs:
            path_list: list - A list of path names
        Returns:
            ret_val: str - A comma seperated string of the path names from the input

        Concatenate all the file names that an article has been extracted from into a single comma seperated string
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

    def __convert_to_word_frequency_JSON_object__(self, title: str, extracted_from: str) -> None:
        """
        Inputs:
            title: str - The title of the article that had word frequency done
            extracted_from: str - A single comma seperated string of the path names the article was extracted from
        
        Converts the word counting data into an class instance for sending to the Data layer
        """
        frequency_data = self.tf[title]
        frequency_object = __WordFrequency__(title, extracted_from, frequency_data)

        if frequency_object.document_title == '':
            print('Found empty title. Skipping', 'debug')
            return

        json_object = json.dumps(frequency_object, cls=__WordFrequencyEncoder__, sort_keys=True, indent=4,
                                 ensure_ascii=False)

        self.word_frequencies_ready_for_sending.append(json_object)

    def __reset__(self, hard_reset=False):
        """
        Inputs:
            hard_reset: bool - Indicates whether a hard reset of the handler should be done, removing all pending word counts not sent yet (default: False)
        
        Resets the WordFrequencyHandler to ready it for processing the next article
        """
        self.tf = TermFrequency()
        if hard_reset:
            self.word_frequencies_ready_for_sending = []

    def get_next_pending_wordcount(self):
        """
        Returns the next pending word count
        """
        return self.word_frequencies_ready_for_sending.pop()

    def __create_file_back_up__(self, file_name: str, error_dir: str) -> None:
        """
        Inputs:
            file_name: str - Name of the backup file to create
            error_dir: str - The relative path from project root to create backup file
        
        Writes the content of pending word count data to a JSON file with the specified name in the specified directory
        """
        if not error_dir:
            raise EnvironmentError(f'Environment Variable <{Ev.instance.ERROR_DIRECTORY}> not specified...')

        file_path: str = error_dir + self.back_up_file_prefix + file_name

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('{\n')
            file.write('\t\"back_up\": [\n')
            count_max = len(self.word_frequencies_ready_for_sending)
            count_current = 1
            for sending_json in self.word_frequencies_ready_for_sending:
                file.write(sending_json)
                if count_current < count_max:
                    file.write(',')
                file.write('\n')
                count_current += 1

            file.write('\t]\n}')


class __WordFrequency__:
    """
    Parent wrapper class holding the word count data transformed into JSON
    """

    def __init__(self, title: str, extracted_from: str, frequency_data: List) -> None:
        self.words: List = []
        for word in frequency_data:
            if word == '':
                print('Found empty word, skipping...', 'debug')
                continue

            count = frequency_data[word]
            self.words.append(__Word__(word, count))

        self.document_title: str = title
        self.filepath: str = extracted_from


class __Word__:
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
