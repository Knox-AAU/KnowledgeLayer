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

def processStoredPublications(content):
        # Classify documents and call appropriate pre-processor
        document: Document = document_classifier.classify(content)

        # Wordcount the lemmatized data and create Data Transfer Objects
        dtos = []
        for article in document.articles:
            word_counts = WordCounter.count_words(article.body)
            dto = DocumentWordCountDto(article.title, article.path, word_counts[0], word_counts[1], document.publisher)
            dtos.append(dto)

        # Send word count data to database
        try:
            WordCountDao.send_word_count(dtos)
        except ConnectionError as error:
            raise error
        except Exception as error:
            raise error
def pipeline():
    if __name__ == "__main__":
        PipelineManager().run_pipeline()
