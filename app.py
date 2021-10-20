import json
import threading
import os
import sched
import time

from os.path import exists
from word_count import WordFrequencyHandler
from doc_classification import DocumentClassifier
from api import ImportApi
import uvicorn
from environment import EnvironmentVariables as Ev

# Instantiate EnvironmentVariables class for future use. Environment constants cannot be accessed without this
Ev()

# The instantiation of the word counter
word_counter = WordFrequencyHandler()

# Makes a directory for the queue (Also done in the api). Only runs once.
filePath = Ev.instance.get_value(Ev.instance.QUEUE_DIRECTORY)
if not exists(filePath):
    os.mkdir(filePath)

# Instantiation of the scheduler
s = sched.scheduler(time.time, time.sleep)


def run_api():
    uvicorn.run(ImportApi.app, host="0.0.0.0")


def process_stored_publications(sc):
    """
    This function processes the stored articles and manuals from Grundfos and Nordjyske.
    This includes the extraction of data from the .json files, the lemmatization and wordcount,
    uploading data to the database.
    
    :param sc: scheduler
    """
    # TODO Test this function when all the components are done
    # Creates a list of all files in the folder defined as filePath.
    list_of_files = os.listdir(filePath)

    for file in list_of_files:

        with open(filePath + file) as json_file:
            content = json.load(json_file)

        # Classify documents and call appropriate pre-processor
        document = DocumentClassifier.classify(content)

        # Wordcount the lemmatized data
        # TODO: Word count
        word_counter.word_count_document("DOCTITLE", "TEXT_BODY", ["PathList"])
        try:
            print(str(word_counter.get_next_pending_wordcount()))
        except IndexError:
            print("No elements")
        # Word counts can then be accessed with: word_counter[DOCTITLE][TERM]

        # TODO: (Out of scope for now) Construct knowledge graph depending on document type

        # TODO: Upload to database

        # Removes the current file that has been processed
        os.remove(filePath + file)
        print(filePath + file + " Has been processed")

    print("No more files! \nWaiting for 30 seconds before rerun.")
    s.enter(30, 1, process_stored_publications, (sc,))


def pipeline():
    print("Beginning of Knowledge Layer!")

    # Start a separate thread for the API to avoid blocking
    api_thread = threading.Thread(target=run_api)
    api_thread.start()

    s.enter(30, 1, process_stored_publications, (s,))
    s.run()

    print("End of Knowledge Layer!")


if __name__ == "__main__":
    pipeline()
