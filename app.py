import json
import threading
import os
import sched
import time
import logging

from os.path import exists
from word_count import WordFrequencyHandler
from doc_classification import DocumentClassifier
from api import ImportApi
import uvicorn

# The instantiation of the work counter
word_counter = WordFrequencyHandler()

# Makes a directory for the queue (Also done in the api). Only runs once.
filePath = "./queue/"
if not exists(filePath):
    os.mkdir(filePath)

#Instantiation of the scheduler
s = sched.scheduler(time.time, time.sleep)

# Instantiation of logging functionalities 
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

def runApi():
    uvicorn.run(ImportApi.app, host="0.0.0.0")

'''
processStoredPublications:

This function processes the stored articles and manuals from Grundfos and Nordjyske.
This includes the extraction of data from the .json files, the lemmatization and wordcount,
uploading data to the database.

:param sc: scheduler
:return: No return
'''
def processStoredPublications(sc):
    # TODO Test this function when all the components are done
    #Creates a list of all files in the folder defined as filePath.
    listOfFiles = os.listdir(filePath)

    for file in listOfFiles:

        with open(filePath + file) as json_file:
            content = json.load(json_file)

        # Classify documents and call appropriate pre-processor
        document = DocumentClassifier.classify(content)

        # TODO: Lemmatization of some form

        # Run the processed data through the kemmatizer
        # TODO: Lemmatization of some form

        # Wordcount the lemmatized data
        # TODO: Word count
        word_counter.do_word_count_for_article("DOCTITLE", "TEXT_BODY", ["PathList"])
        try:
            print(str(word_counter.get_next_pending_wordcount()))
        except IndexError:
            print("No elements")
        # Word counts can then be accessed with: word_counter[DOCTITLE][TERM]

        # TODO: (Out of scope for now) Construct knowledge graph depending on document type

        # TODO: Upload to database

        #Removes the current file that has been processed
        os.remove(filePath + file)
        logger.warning(filePath + file + " Has been processed")

    logger.warning("No more files! \nWaiting for 30 seconds before rerun.")
    s.enter(5, 1, processStoredPublications, (sc,))

def pipeline():
    print("Beginning of Knowledge Layer!")

    #Start a seperate thread for the API to avoid blocking
    api_thread = threading.Thread(target=runApi)
    api_thread.start()

    s.enter(5, 1, processStoredPublications, (s,))
    s.run()

    print("End of Knowledge Layer!")


if __name__ == "__main__":
    pipeline()
