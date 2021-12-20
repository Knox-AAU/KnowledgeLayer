import json
import threading
import os
import sched
import time

import requests
import uvicorn
from scheduler import scheduler
from os.path import exists
from doc_classification import DocumentClassifier, Document
from api import ImportApi
from data_access.data_transfer_objects.DocumentWordCountDto import DocumentWordCountDto
from environment import EnvironmentVariables as Ev
from word_count.WordCounter import WordCounter
from data_access import WordCountDao
from utils import logging

# Instantiate EnvironmentVariables class for future use. Environment constants cannot be accessed without this
Ev()


# Makes a directory for the queue (Also done in the api). Only runs once.
filePath = Ev.instance.get_value(Ev.instance.QUEUE_PATH)
if not exists(filePath):
    os.mkdir(filePath)

# Instantiation of the scheduler
s = sched.scheduler(time.time, time.sleep)

# Instantiate DocumentClassifier
document_classifier = DocumentClassifier()

def run_api():
    """

    """
    uvicorn.run(ImportApi.app, host="0.0.0.0")


def process_stored_publications(content):
    """
    This function processes the stored articles and manuals from Grundfos and Nordjyske.
    This includes the extraction of data from the .json files, the lemmatization, wordcount, and
    uploading data to the database.

    :param content: The input JSON file
    """
    # Classify documents and call appropriate pre-processor
    document: Document = document_classifier.classify(content)
    total_number_of_articles = len(document.articles)
    total_number_of_processed_articles = 0
    # Wordcount the lemmatized data and create Data Transfer Objects
    dtos = []
    for article in document.articles:
        logging.LogF.log(f"{int((total_number_of_processed_articles*100)/total_number_of_articles)}% : Word counting for {document.publisher} - {article.title}")
        word_counts = WordCounter.count_words(article.title + " " + article.body)
        dto = DocumentWordCountDto(article.title, article.path, word_counts[0], word_counts[1], document.publisher)
        dtos.append(dto)
        total_number_of_processed_articles += 1

    logging.LogF.log(f"100% : Word counting for {document.publisher}")

    logging.LogF.log(f"Sending {document.publisher}")
    # Send word count data to database
    try:
        WordCountDao.send_word_count(dtos)
    except ConnectionError as error:
        raise error
    except Exception as error:
        raise error


def pipeline():
    """
    The main function and entry point of the Knowledge Layer.
    """
    print("Beginning of Knowledge Layer!")

    # Start a seperate thread for the API to avoid blocking
    api_thread = threading.Thread(target=run_api)
    api_thread.start()

    s.enter(5, 1, scheduler, (s, process_stored_publications))
    s.run()
    print("End of Knowledge Layer!")


if __name__ == "__main__":
    pipeline()
