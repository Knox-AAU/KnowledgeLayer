import os
import uuid

from fastapi import FastAPI, Request, HTTPException
import time
from os.path import exists
import json
from environment.EnvironmentConstants import EnvironmentVariables as Ev

Ev()

class FileWriter:
    """

    """
    async def add_to_queue(self, request: Request) -> None:
        """
        Adds the request to a file queue
        :param request: The post request sent the endpoint
        :return: None
        """
        queue_path: str = Ev.instance.get_value(Ev.instance.QUEUE_PATH)

        unix_time: int = int(time.time())
        file_name: str = str(uuid.uuid4()) + str(unix_time)+".json"

        with open(queue_path + file_name, "w", encoding="utf-8") as f:
            f.write(json.dumps(await request.json()))