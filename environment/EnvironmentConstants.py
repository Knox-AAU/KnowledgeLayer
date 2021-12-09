# from __future__ import annotations
from dotenv import load_dotenv
import os


class EnvironmentVariables:
    """
    The singleton Environment wrapper for the inner class
    """
    class __EnvironmentVariables:
        """
        The inner class with only one instance
        """
        def __init__(self):
            self.QUEUE_PATH = "QUEUE_PATH"
            self.NJ_SPACY_MODEL = "NJ_SPACY_MODEL"
            self.GF_SPACY_MODEL = "GF_SPACY_MODEL"
            self.LEMMATIZER_ENDPOINT = "LEMMATIZER_ENDPOINT"
            self.WORD_COUNT_DATA_ENDPOINT = "WORD_COUNT_DATA_ENDPOINT"
            self.ONTOLOGY_NAMESPACE = "ONTOLOGY_NAMESPACE"
            self.TRIPLE_DATA_ENDPOINT = "TRIPLE_DATA_ENDPOINT"
            self.GF_PATTERN_PATH = "GF_PATTERN_PATH"
            load_dotenv()

        def get_value(self, key: str, default = None):
            """
            Reads the .env file and returns the requested value.

            :param key: The key to look up in the .env file
            :param default: The default value to put if no value is found for the key
            :return: The value for the given key as a string
            """
            return os.environ.get(key) if os.environ.get(key) is not None else default
    
    instance: __EnvironmentVariables = None

    def __new__(cls):
        """
        Overrides __new__ dunder method to return the instance of the inner class each time an object is called.
        This is where the singleton magic is happening.
        """
        if not EnvironmentVariables.instance:
            EnvironmentVariables.instance = EnvironmentVariables.__EnvironmentVariables()
        return EnvironmentVariables.instance
