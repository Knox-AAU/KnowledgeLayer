import datetime
import uvicorn
from fastapi import FastAPI, Request
import threading
import logging

from publication_generator import PublicationGenerator
from performace_test_suite import PerformanceTestSuite
from doc_classification import PipelineManager
from unittest.mock import patch

logger = logging.getLogger()
import data_access.WordCountDao


def open_mock_endpoints():
    async def lemma_mock(request: Request):
        content = await request.json()
        return {'lemmatized_string': content['string']}

    app = FastAPI()
    app.post("/lemmatizer")(lemma_mock)
    app.post('/wordcount')(lambda: 200)
    return threading.Thread(target=uvicorn.run, args=(app,), kwargs=dict(host="0.0.0.0", port=5000))


def make_generator(paragraph_word_count):
    generator = PublicationGenerator("NJ")
    generator.repeat_amount = 20
    generator.stop_word_density = 0.5
    generator.article_amount = 2
    generator.paragraph_amount = 2
    generator.paragraph_word_count = paragraph_word_count
    return generator


@patch('pre_processing.PreProcessor.lemmatize')
@patch('data_access.WordCountDao.send_word_count')
def run_tests(mock_lemma, mock_send_word):
    pipeline = PipelineManager()
    mock_lemma.side_effect = lambda x, y: x
    mock_send_word.return_value = None
    suite = PerformanceTestSuite(pipeline.processStoredPublications, make_generator(10).publication_generator())

    # with open(f'test_{datetime.datetime.now().date()}_2.txt', "a") as f:
    #     f.write(str(suite.run()))
    for i in range(10):
        generator = make_generator(i * 100)
        suite.data_generator = generator.publication_generator()
        print(str(suite.run()))
    #
    # wordcount = generator.article_amount * generator.paragraph_amount * generator.paragraph_word_count
    # data = suite.run()
    # import numpy as np
    # print(((len(data) - 1) * wordcount) / np.array(data[1:]).sum())


if __name__ == "__main__":
    run_tests()
