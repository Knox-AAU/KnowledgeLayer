import json
import logging
import threading
import os
import sched
import time

import requests
import uvicorn
from scheduler import scheduler
from os.path import exists
from word_count import WordFrequencyHandler
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

# The instantiation of the word counter
word_counter = WordFrequencyHandler()

# Makes a directory for the queue (Also done in the api). Only runs once.
filePath = Ev.instance.get_value(Ev.instance.QUEUE_PATH)
if not exists(filePath):
    os.mkdir(filePath)

# Instantiation of the scheduler
s = sched.scheduler(time.time, time.sleep)

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
        document: Document = DocumentClassifier.classify(content)

        # Wordcount the lemmatized data
        # TODO: Word count

        for article in document.content.articles:
            content = ' '.join([ paragraph.value for paragraph in article.paragraphs])
            word_counter.word_count_document(article.headline, content, article.extracted_from, document.content.publication)

        logger.warning(word_counter.word_frequencies_ready_for_sending)

        request_body = [v for v in word_counter.entry_generator()]
        #
        # try:
        #     print(str(request_body))
        # except IndexError:
        #     print("No elements")
        # Word counts can then be accessed with: word_counter[DOCTITLE][TERM]
        db_endpoint = Ev.instance.get_value(Ev.instance.WORD_COUNT_DATA_ENDPOINT)
        try:
            requests.post(db_endpoint, json=request_body)
        except Exception as e:
            print(e)
            
        # TODO: (Out of scope for now) Construct knowledge graph depending on document type

        # TODO: Upload to database
        word_count_dto = \
            DocumentWordCountDto(document.title, document.paths, word_counts[0], word_counts[1], document.publisher)
        WordCountDao.send_word_count([word_count_dto])

def pipeline():
    print("Beginning of Knowledge Layer!")

    #Start a seperate thread for the API to avoid blocking
    api_thread = threading.Thread(target=run_api)
    api_thread.start()

    s.enter(5, 1, scheduler, (s, processStoredPublications))
    s.run()
    print("End of Knowledge Layer!")

if __name__ == "__main__":
    pipeline()
