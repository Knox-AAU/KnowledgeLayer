import os
from os.path import exists
import time
from fastapi import FastAPI, Request, HTTPException
from knox_source_data_io.io_handler import IOHandler, Generator
import json
import uvicorn

app = FastAPI()
handler = IOHandler(Generator(app="This app", version=1.0), "https://repos.knox.cs.aau.dk/schema/publication.schema.json")

filePath = "./queue/"
if not exists(filePath):
    os.mkdir(filePath)

@app.post("/uploadJsonDoc/",status_code=200)
async def read_doc(jsondoc: Request):
    data = await jsondoc.body()

    try:
        json.loads(data, object_hook=IOHandler.convert_dict_to_obj)
    except:
        raise HTTPException(status_code=403, detail="Json file not following schema")

    unixTime = int(time.time())
    fileName = str(unixTime)+".json"

    with open(filePath+fileName, "w", encoding="utf-8") as f:
        f.write(json.dumps(await jsondoc.json()))

    return "Json file successfully created"