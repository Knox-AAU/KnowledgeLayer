import json
from utils.logging import LogF
import os
import sched
import time

from os.path import exists
from typing import Callable

from environment import EnvironmentVariables as Ev

# Instantiate EnvironmentVariables class for future use. Environment constants cannot be accessed without this
Ev()


# Instantiation of logging functionalities
class IntervalScheduler:
    def __init__(self, interval: int, callback: Callable):
        self.scheduler_instance = sched.scheduler(time.time, time.sleep)
        self.interval = interval
        self.callback = callback
        # Makes a directory for the queue (Also done in the api). Only runs once.
        self.filePath = Ev.instance.get_value(Ev.instance.QUEUE_PATH)
        if not exists(self.filePath):
            os.mkdir(self.filePath)

    def queue(self, callBack):
        # Creates a list of all files in the folder defined as filePath.
        listOfFiles = os.listdir(self.filePath)

        for file in sorted(listOfFiles):
            with open(self.filePath + file) as json_file:
                content = json.load(json_file)

            try:
                callBack(content)

                # Removes the current file that has been processed
                os.remove(self.filePath + file)

                LogF.log(self.filePath + file + " Has been processed")
            except ConnectionError as error:
                LogF.log("Connection error: Adding to queue again")
            except Exception as error:
                LogF.log("Unexpected error: Removed from queue")
                os.remove(self.filePath + file)

    def __scheduler(self):
        LogF.log(f"No more files! \nWaiting for {self.interval} seconds before rerun.")
        self.queue(self.callback)
        self.scheduler_instance.enter(self.interval, 1, self.__scheduler)

    def run(self, run_initial: bool = False):
        if run_initial:
            self.queue(self.callback)
        self.scheduler_instance.enter(self.interval, 1, self.__scheduler)
        self.scheduler_instance.run()
