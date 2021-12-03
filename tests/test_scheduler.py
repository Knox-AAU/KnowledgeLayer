import math
import sched
from scheduler import queue
import time
from environment import EnvironmentVariables as Ev

# Instantiate EnvironmentVariables class for future use. Environment constants cannot be accessed without this
Ev()

# Instantiation of the scheduler
s = sched.scheduler(time.time, time.sleep)

# The content to be asserted
assertContent = []

def generate_mock_data(numberOfFiles: int):
    filePath = Ev.instance.get_value(Ev.instance.QUEUE_PATH)
    unixTime = 0

    for n in range(numberOfFiles):
        unixTime = unixTime + 1

        with open(filePath + str(unixTime).zfill(1 + int(math.log10(numberOfFiles))) + ".json", "w", encoding="utf-8") as file:
            file.write('{ "num": "' + str(n) + '"}')


def file_checker(content):
    assertContent.append(int(content["num"]))


def test_Scheduler_FIFO_principle():
    generate_mock_data(5000)
    check_array = [i for i in range(5000)]
    queue(file_checker)
    # Assert test for one file
    for i in assertContent:
        assert i == check_array[i]
