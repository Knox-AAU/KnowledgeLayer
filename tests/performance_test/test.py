import datetime
import uvicorn
from fastapi import FastAPI, Request
import threading
import logging

from publication_generator import PublicationGenerator
from performace_test_suite import PerformanceTestSuite
from doc_classification import PipelineManager

logger = logging.getLogger()

def open_mock_endpoints():
    async def lemma_mock(request: Request):
        content = await request.json()
        return {'lemmatized_string': content['string']}

    app = FastAPI()
    app.post("/lemmatizer")(lemma_mock)
    app.post('/wordcount')(lambda: 200)
    return threading.Thread(target=uvicorn.run, args=(app,), kwargs=dict(host="0.0.0.0", port=5000))


def run_tests():
    generator = PublicationGenerator("NJ")
    generator.repeat_amount = 20
    generator.stop_word_density = 0.5
    pipeline = PipelineManager()
    suite = PerformanceTestSuite(pipeline.processStoredPublications, generator.publication_generator())
    mock_endpoint_thread = open_mock_endpoints()
    suite.setup_suite_func = lambda: mock_endpoint_thread.start()
    with open(f'test_{datetime.datetime.now().date()}_2.txt', "a") as f:
        f.write(str(suite.run()))


if __name__ == "__main__":
    run_tests()
