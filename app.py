import json
import threading
import os
import time

from os.path import exists
from word_count import WordFrequencyHandler
from doc_classification import *
from api import ImportApi
import uvicorn

word_counter = WordFrequencyHandler()

# Makes a directory for the queue (Also done in the api). Only runs once.
filePath = "./queue/"
if not exists(filePath):
    os.mkdir(filePath)

def runApi():
    uvicorn.run(ImportApi.app, host="0.0.0.0")

def processApiInput(listOfFiles):
    for item in listOfFiles:

        with open(filePath + item) as json_file:
            content = json.load(json_file)

        # Classify documents and call appropriate pre-processor
        document = DocumentClassifier.classify(content)

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

def pipeline():
    print("Beginning of Knowledge Layer!")

    #Start a seperate thread for the API to avoid blocking
    api_thread = threading.Thread(target=runApi)
    api_thread.start()

    #while True:
    listOfFiles = os.listdir(filePath)
    if not len(listOfFiles) == 0:
        print("Process api input")
        processApiInput(listOfFiles)
    else:
        print("Filepath empty, waiting 30 seconds")
        time.sleep(30)


    print("End of Knowledge Layer!")


if __name__ == "__main__":
    pipeline()
