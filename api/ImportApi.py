from fastapi import FastAPI, Request, HTTPException
from knox_source_data_io.io_handler import IOHandler
from file_io.FileWriter import FileWriter
import os
import spacy
from spacy import displacy
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
file_writer = FileWriter()

publisher_to_model = {
    'NJ': spacy.load('da_core_news_lg'),
    'GF': spacy.load('en_core_web_sm')
}
#
# origin = { "http://localhost:3000" }
#
# app.add_middleware(CORSMiddleware,
#                    allow_origins=origin,
#                    allow_credentials=True,
#                    allow_methods=['*'],
#                    allow_headers=['*'])


@app.post("/uploadJsonDoc/", status_code=200)
async def read_doc(request: Request):
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        IOHandler.validate_json(await request.json(), os.path.join(path, '..', 'schema.json'))
    except Exception as e:
        raise HTTPException(status_code=403, detail="Json file not following schema with error: " + str(e))
    try:
        await file_writer.add_to_queue(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail="File not added to queue with error: " + str(e))

    return "Json file successfully created"


@app.post("/visualiseNer/", status_code=200)
async def visualise(request: Request):
    try:
        json = await request.json()
        publisher, text = json['publisher'], json['text']
        nlp = publisher_to_model[publisher]
        doc = nlp(text)
        html = displacy.render(doc, style="ent", minify=True)
        return html
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to visualise: " + str(e))
