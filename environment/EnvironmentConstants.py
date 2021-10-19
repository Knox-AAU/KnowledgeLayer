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
            # self.INPUT_DIRECTORY = "INPUT_DIRECTORY"
            # self.OUTPUT_DIRECTORY = "OUTPUT_DIRECTORY"
            # self.ERROR_DIRECTORY = "ERROR_DIRECTORY"
            # self.RDF_OUTPUT_FOLDER = "RDF_OUTPUT_FOLDER"
            # self.OUTPUT_FORMAT = "OUTPUT_FORMAT"
            # self.OUTPUT_FILE_NAME = "OUTPUT_FILE_NAME"
            # self.ONTOLOGY_FILEPATH = "ONTOLOGY_FILEPATH"
            # self.TRIPLE_DATA_ENDPOINT = "TRIPLE_DATA_ENDPOINT"
            self.QUEUE_DIRECTORY = "QUEUE_DIRECTORY"
            self.WORD_COUNT_DATA_ENDPOINT = "WORD_COUNT_DATA_ENDPOINT"
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
