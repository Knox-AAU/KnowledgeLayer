from fastapi import FastAPI, Request, HTTPException
from knox_source_data_io.io_handler import IOHandler
from file_io.FileWriter import FileWriter
import os

app = FastAPI()
file_writer = FileWriter()

@app.post("/uploadJsonDoc/",status_code=200)
async def read_doc(request: Request):
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        IOHandler.validate_json(await request.json(), os.path.join(path, '..', 'schema.json'))
    except Exception as e:
        raise HTTPException(status_code=403, detail="Json file not following schema with error: " + e)
    try:
        await file_writer.add_to_queue(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail="File not added to queue with error: " + e)

    return "Json file successfully created"