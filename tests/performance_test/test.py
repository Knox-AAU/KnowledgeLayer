import datetime
import os
import uvicorn
from fastapi import FastAPI, Request
import threading
import logging
from api.ImportApi import read_doc, app

from publication_generator import PublicationGenerator
from performace_test_suite import PerformanceTestSuite
from doc_classification import PipelineManager
from unittest.mock import patch
from fastapi.testclient import TestClient
from knox_source_data_io.io_handler import IOHandler

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


def make_generator(paragraph_amount, word_count, stop_dens):
    generator = PublicationGenerator("NJ")
    generator.repeat_amount = 5
    generator.stop_word_density = stop_dens/10
    generator.article_amount = 2
    generator.paragraph_amount = paragraph_amount
    generator.paragraph_word_count = word_count
    return generator


@patch('data_access.WordCountDao.send_word_count')
@patch('pre_processing.PreProcessor.lemmatize')
def run_tests(mock_lemma, mock_send_word):
    pipeline = PipelineManager()
    mock_lemma.side_effect = lambda x, y: x
    mock_send_word.return_value = None
    suite = PerformanceTestSuite(pipeline.processStoredPublications, make_generator(0, 0, 0).publication_generator())

    # with open(f'test_{datetime.datetime.now().date()}_2.txt', "a") as f:
    #     f.write(str(suite.run()))
    generator = PublicationGenerator("NJ")
    generator.repeat_amount = 5
    generator.article_amount = 2
    with open('./test_overall.csv', 'a') as f:
        f.write("paragraph_amount;word_count;stop_dens;data\n")
        for paragraph_amount in range(1, 11):
            for word_count in range(100, 1100, 100):
                for stop_dens in range(11):
                    generator.stop_word_density = stop_dens/10
                    generator.paragraph_amount = paragraph_amount
                    generator.paragraph_word_count = word_count
                    generator.set_seed(paragraph_amount+word_count+stop_dens)
                    suite.data_generator = generator.publication_generator()
                    f.write(f'{paragraph_amount};{word_count};{stop_dens};{suite.run()}\n')
    #
    # wordcount = generator.article_amount * generator.paragraph_amount * generator.paragraph_word_count
    # data = suite.run()
    # import numpy as np
    # print(((len(data) - 1) * wordcount) / np.array(data[1:]).sum())

# @patch('file_io.FileWriter.FileWriter.add_to_queue')
# def read_doc_benchmark(mock_queue):
#     mock_queue.return_value = None
#     client = TestClient(app);
#     test_func = lambda json: client.post("/uploadJsonDoc/", json)
#     suite = PerformanceTestSuite(test_func, None)
#     with open('./test_read_doc.csv', 'a') as f:
#         f.write("paragraph_amount;article_amount;data\n")
#         for paragraph_amount in range(1, 11):
#             for article_amount in range(1, 11):
#                 generator = PublicationGenerator("NJ", paragraph_amount = paragraph_amount,
#                                                  article_amount = article_amount, paragraph_word_count = 10)
#                 generator.set_seed(paragraph_amount + article_amount)
#                 suite.data_generator = generator.publication_generator()
#                 f.write(f'{paragraph_amount};{article_amount};{suite.run()}\n')


def read_doc_benchmark():
    path = os.path.dirname(os.path.abspath(__file__))
    test_func = lambda json: IOHandler.validate_json(json, os.path.join(path, '../..', 'schema.json'))
    suite = PerformanceTestSuite(test_func, None)
    with open('./test_read_doc.csv', 'a') as f:
        f.write("paragraph_amount;article_amount;data\n")
        for paragraph_amount in range(1, 11):
            for article_amount in range(1, 11):
                generator = PublicationGenerator("NJ", paragraph_amount = paragraph_amount,
                                                 article_amount = article_amount, paragraph_word_count = 10)
                generator.set_seed(paragraph_amount + article_amount)
                suite.data_generator = generator.publication_generator()
                f.write(f'{paragraph_amount};{article_amount};{suite.run()}\n')

if __name__ == "__main__":
    #run_tests()
    read_doc_benchmark()
