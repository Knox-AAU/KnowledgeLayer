import json
import logging
import os
import sched
import time

from os.path import exists

# Instantiation of the scheduler
s = sched.scheduler(time.time, time.sleep)

# Instantiation of logging functionalities
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

# Makes a directory for the queue (Also done in the api). Only runs once.
filePath = "./queue/"
if not exists(filePath):
    os.mkdir(filePath)


def queue(sc, callBack):
    # Creates a list of all files in the folder defined as filePath.
    listOfFiles = os.listdir(filePath)

    for file in listOfFiles:
        with open(filePath + file) as json_file:
            content = json.load(json_file)

        callBack(content)

        #Removes the current file that has been processed
        os.remove(filePath + file)
        logger.warning(filePath + file + " Has been processed")

    logger.warning("No more files! \nWaiting for 30 seconds before rerun.")
    s.enter(5, 1, queue, (sc, callBack))