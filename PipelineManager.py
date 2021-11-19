import os
import threading
from os.path import exists

import uvicorn

from api import ImportApi
from data_access import WordCountDao
from data_access.data_transfer_objects.DocumentWordCountDto import DocumentWordCountDto
from doc_classification import DocumentClassifier
from model.Document import Document
from environment import EnvironmentVariables as Ev
from utils.scheduler import IntervalScheduler
from utils import LogF
from word_count import WordCounter

Ev()


class PipelineManager:

    def __init__(self):
        # Makes a directory for the queue (Also done in the api). Only runs once.
        self.filePath = Ev.instance.get_value(Ev.instance.QUEUE_PATH)
        if not exists(self.filePath):
            os.mkdir(self.filePath)

        # Instantiante DocumentClassifier
        self.document_classifier = DocumentClassifier()

    def processStoredPublications(self, content):
        # Classify documents and call appropriate pre-processor
        document: Document = self.document_classifier.classify(content)
        total_number_of_articles = len(document.articles)
        total_number_of_processed_articles = 0
        # Wordcount the lemmatized data and create Data Transfer Objects
        dtos = []
        for article in document.articles:
            LogF.log(f"{int((total_number_of_processed_articles * 100) / total_number_of_articles)}% : "
                     f"Word counting for {document.publisher} - {article.title}")
            word_counts = WordCounter.count_words(article.title + " " + article.body)
            dto = DocumentWordCountDto(article.title, article.path, word_counts[0], word_counts[1], document.publisher)
            dtos.append(dto)
            total_number_of_processed_articles += 1

        LogF.log(f"100% : Word counting for {document.publisher}")

        LogF.log(f"Sending {document.publisher}")
        # Send word count data to database
        try:
            WordCountDao.send_word_count(dtos)
        except ConnectionError as error:
            raise error
        except Exception as error:
            raise error

    def run_api(self):
        uvicorn.run(ImportApi.app, port=8000, host="0.0.0.0")

    def run_pipeline(self):
        LogF.log("Beginning of Knowledge Layer!")
        api_thread = threading.Thread(target=self.run_api)
        api_thread.start()

        IntervalScheduler(30, self.processStoredPublications).run(True)
        # threading.Thread(target=sched.run, args=(True,)).run()
        print("End of Knowledge Layer!")
