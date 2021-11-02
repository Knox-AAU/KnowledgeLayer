import json
import logging
import threading
import os
import sched
import time

import requests
import uvicorn

from doc_classification.PipelineManager import PipelineManager
from scheduler import scheduler
from os.path import exists
from doc_classification import DocumentClassifier, Document
from api import ImportApi
from data_access.data_transfer_objects.DocumentWordCountDto import DocumentWordCountDto
from environment import EnvironmentVariables as Ev
# Instantiate EnvironmentVariables class for future use. Environment constants cannot be accessed without this
from word_count.WordCounter import WordCounter
from data_access import WordCountDao

Ev()

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)


def run_api():
    uvicorn.run(ImportApi.app, host="0.0.0.0")

    """
    This function processes the stored articles and manuals from Grundfos and Nordjyske.
    This includes the extraction of data from the .json files, the lemmatization and wordcount,
    uploading data to the database.
    
    :param content: json file
    :return: No return
    """


def pipeline():
    if __name__ == "__main__":
        PipelineManager().run_pipeline()
