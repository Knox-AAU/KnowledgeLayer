import json
from utils import logging
import os

from os.path import exists
from environment import EnvironmentVariables as Ev

# Instantiate EnvironmentVariables class for future use. Environment constants cannot be accessed without this
Ev()

# Makes a directory for the queue (Also done in the api). Only runs once.
filePath = Ev.instance.get_value(Ev.instance.QUEUE_PATH)
if not exists(filePath):
    os.mkdir(filePath)


def queue(callBack):
    # Creates a list of all files in the folder defined as filePath.
    list_of_files = os.listdir(filePath)

    for file in sorted(list_of_files):

        try:
            with open(filePath + file) as json_file:
                content = json.load(json_file)

            callBack(content)

            # Removes the current file that has been processed
            os.remove(filePath + file)

            logging.LogF.log(filePath + file + " has been processed")

            logging.LogF.log(f"{len(os.listdir(filePath))} files left in queue")
            # logging.LogF.log(f"{processed}/{len(list_of_files)} files processed")
        except ConnectionError as error:
            logging.LogF.log("Connection error: Adding to queue again")
        except Exception as error:
            logging.LogF.log("Unexpected error: Removed from queue")
            logging.LogF.log("Error with message: " + str(error))
            os.remove(filePath + file)


def scheduler(sc, callBack):
    logging.LogF.log("No more files! \nWaiting for 30 seconds before rerun.")
    queue(callBack)
    sc.enter(30, 1, scheduler, (sc, callBack))