from fastapi import FastAPI, Request, HTTPException
from knox_source_data_io.io_handler import IOHandler, Generator
from knox_source_data_io.models.wrapper import Wrapper
from file_io.FileWriter import FileWriter
import json

app = FastAPI()
file_writer = FileWriter()
handler = IOHandler(Generator(app="This app", version=1.0), "./schema.json")

@app.post("/uploadJsonDoc/",status_code=200)
async def read_doc(request: Request):
    data = await request.body()

    IOHandler.validate_json(await request.json(), "./schema.json")
    try:
        print("hello")
        #json.loads(data, object_hook=IOHandler.convert_dict_to_obj)
    except:
        raise HTTPException(status_code=403, detail="Json file not following schema")

    try:
        await file_writer.add_to_queue(request)
    except:
        raise HTTPException(status_code=500, detail="File not added to queue")

    return "Json file successfully created"