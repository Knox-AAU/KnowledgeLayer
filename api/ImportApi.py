from fastapi import FastAPI, Request, HTTPException
from knox_source_data_io.io_handler import IOHandler
from file_io.FileWriter import FileWriter
import os
import spacy
from spacy import displacy

from model import Document, Article
from rdf import NJTripleExtractor, GFTripleExtractor
from environment import EnvironmentVariables as Ev
Ev()


from utils import load_model, logging
from environment import EnvironmentVariables as Ev
Ev()

app = FastAPI()
file_writer = FileWriter()

publisher_to_model = {
    'NJ': spacy.load('da_core_news_lg'),
    'GF': spacy.load(Ev.instance.get_value(Ev.instance.GF_SPACY_MODEL))
}

publisher_to_triple_extractor = {
    'NJ': NJTripleExtractor(Ev.instance.get_value(Ev.instance.NJ_SPACY_MODEL)),
    'GF': GFTripleExtractor(Ev.instance.get_value(Ev.instance.GF_SPACY_MODEL))
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


@app.post("/generateKG/", status_code=200)
async def genKG(request: Request):
    """
    Backend for 'Show Triples' functionality in the UI

    :param request: The request object, containing the POST content
    :return: A stringified version of the generated triples, or status code 500
    """
    try:
        json = await request.json()
        publisher, text = json['publisher'], json['text']
        triple_extractor = publisher_to_triple_extractor[publisher]
        triple_extractor.clear_stored_triples()
        # triple_extractor = GFTripleExtractor(Ev.instance.get_value(Ev.instance.GF_SPACY_MODEL))
        document = Document(publisher)
        article = Article("SampleTitle", text, "SamplePath", article_id="SampleID")
        document.articles.append(article)
        ttl_file = triple_extractor.return_ttl(document)
        return str(ttl_file)
    except Exception as e:
        logging.LogF.log(str(e))
        raise HTTPException(status_code=500, detail="Failed generate graph: " + str(e))
