from fastapi import FastAPI, Request, HTTPException
from knox_source_data_io.io_handler import IOHandler, Generator
from knox_source_data_io.models.wrapper import Wrapper
from file_io.FileWriter import FileWriter
import json

app = FastAPI()
file_writer = FileWriter()

@app.post("/uploadJsonDoc/",status_code=200)
async def read_doc(request: Request):
    try:
        IOHandler.validate_json(await request.json(), "../schema.json")
    except:
        raise HTTPException(status_code=403, detail="Json file not following schema")
    try:
        await file_writer.add_to_queue(request)
    except:
        raise HTTPException(status_code=500, detail="File not added to queue")

    return "Json file successfully created"