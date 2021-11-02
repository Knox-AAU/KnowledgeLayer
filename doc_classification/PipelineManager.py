import os
import sched
import threading
import time
from os.path import exists

import uvicorn

from api import ImportApi
from data_access import WordCountDao
from data_access.data_transfer_objects.DocumentWordCountDto import DocumentWordCountDto
from doc_classification import DocumentClassifier
from model.Document import Document
from environment import EnvironmentVariables as Ev
from scheduler import scheduler
from word_count import WordCounter

Ev()


class PipelineManager:

    def __init__(self):
        # Makes a directory for the queue (Also done in the api). Only runs once.
        self.filePath = Ev.instance.get_value(Ev.instance.QUEUE_PATH)
        if not exists(self.filePath):
            os.mkdir(self.filePath)

        # Instantiation of the scheduler
        self.scheduler_instance = sched.scheduler(time.time, time.sleep)

        # Instantiante DocumentClassifier
        self.document_classifier = DocumentClassifier()

    def processStoredPublications(self, content):
        # Classify documents and call appropriate pre-processor
        document: Document = self.document_classifier.classify(content)

        # Wordcount the lemmatized data and create Data Transfer Objects
        dtos = []
        for article in document.articles:
            word_counts = WordCounter.count_words(article.body)
            dto = DocumentWordCountDto(article.title, article.path, word_counts[0], word_counts[1], document.publisher)
            dtos.append(dto)

        # Send word count data to database
        WordCountDao.send_word_count(dtos)

    def run_api(self):
        uvicorn.run(ImportApi.app, host="0.0.0.0")

    def run_pipeline(self):
        print("Beginning of Knowledge Layer!")

        #Start a seperate thread for the API to avoid blocking
        api_thread = threading.Thread(target=self.run_api)
        api_thread.start()

        self.scheduler_instance.enter(5, 1, scheduler, (self.scheduler_instance, self.processStoredPublications))
        self.scheduler_instance.run()
        print("End of Knowledge Layer!")
