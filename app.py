import json
import threading
import os
import sched
import time
import uvicorn
from scheduler import scheduler
from os.path import exists
from word_count import WordFrequencyHandler
from doc_classification import DocumentClassifier
from api import ImportApi
from data_access.data_transfer_objects.DocumentWordCountDto import DocumentWordCountDto
from environment import EnvironmentVariables as Ev
# Instantiate EnvironmentVariables class for future use. Environment constants cannot be accessed without this
from word_count.WordCounter import WordCounter

Ev()

from os.path import exists
from doc_classification import DocumentClassifier, Document
from api import ImportApi
import uvicorn
from data_access import WordCountDao

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
        word_counts = WordCounter.count_words(document.body)

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
