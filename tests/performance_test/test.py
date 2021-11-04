import datetime
import os
from typing import Dict

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
from word_count.WordCounter import WordCounter
from pre_processing.NJPreProcessor import NJPreProcessor
from model.Document import Article

logger = logging.getLogger()
import data_access.WordCountDao
import json
import numpy as np
import re

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
    generator.stop_word_density = stop_dens / 10
    generator.article_amount = 2
    generator.paragraph_amount = paragraph_amount
    generator.paragraph_word_count = word_count
    return generator


@patch('data_access.WordCountDao.send_word_count')
@patch('pre_processing.PreProcessor.lemmatize')
def overall_benchmark(mock_lemma, mock_send_word):
    #benchmark on processStoredPublications()
    pipeline = PipelineManager()
    mock_lemma.side_effect = lambda x, y: x
    mock_send_word.return_value = None
    suite = PerformanceTestSuite(pipeline.processStoredPublications, make_generator(0, 0, 0).publication_generator())

    generator = PublicationGenerator("NJ")
    generator.repeat_amount = 1
    generator.article_amount = 1
    with open('tests/performance_test/output/test_overall.csv', 'a') as f:
        f.write("paragraph_amount;word_count;stop_dens;data\n")
        for paragraph_amount in range(1, 11):
            for word_count in range(100, 1100, 100):
                for stop_dens in range(11):
                    generator.stop_word_density = stop_dens / 10
                    generator.paragraph_amount = paragraph_amount
                    generator.paragraph_word_count = word_count
                    generator.set_seed(paragraph_amount + word_count + stop_dens)
                    suite.data_generator = generator.publication_generator()
                    f.write(f'{paragraph_amount};{word_count};{stop_dens};{suite.run()}\n')
                    logger.warning(f'{paragraph_amount};{word_count};{stop_dens};{suite.run()}\n')


def read_doc_benchmark():
    path = os.path.dirname(os.path.abspath(__file__))
    test_func = lambda json: IOHandler.validate_json(json, os.path.join(path, '../..', 'schema.json'))
    suite = PerformanceTestSuite(test_func, None)
    with open('tests/performance_test/output/test_read_doc.csv', 'a') as f:
        f.write("paragraph_amount;article_amount;data\n")
        for paragraph_amount in range(1, 11):
            for article_amount in range(1, 11):
                generator = PublicationGenerator("NJ", paragraph_amount=paragraph_amount,
                                                 article_amount=article_amount, paragraph_word_count=10)
                generator.set_seed(paragraph_amount + article_amount)
                suite.data_generator = generator.publication_generator()
                f.write(f'{paragraph_amount};{article_amount};{suite.run()}\n')


def word_counter_benchmark():
    wc = WordCounter.count_words

    gen = PublicationGenerator("NJ")
    suite = PerformanceTestSuite(wc, None)
    with open('tests/performance_test/output/test_word_counter.csv', 'a') as f:
        f.write("word_amount;data\n")
        for word_amount in range(100, 1010, 10):
            gen.paragraph_word_count = word_amount
            suite.data_generator = [gen.generate_paragraph()['value']]
            f.write(f'{word_amount};{suite.run()}\n')

def stop_word_benchmark():
    remove_stop_words = NJPreProcessor().remove_stopwords
    suite = PerformanceTestSuite(remove_stop_words, None)

    gen = PublicationGenerator("NJ")
    with open('tests/performance_test/output/test_stop_words.csv', 'a') as f:
        f.write("word_amount;stop_word_dens;data\n")
        for word_amount in range(100, 1100, 100):
            for stop_word_dens in range(11):
                gen.paragraph_word_count = word_amount
                gen.stop_word_density = stop_word_dens/10
                suite.data_generator = [Article("",gen.generate_paragraph()['value'],"")]
                f.write(f'{word_amount};{stop_word_dens/10};{suite.run()}\n')


if __name__ == "__main__":
    #stop_word_benchmark()
    word_counter_benchmark()
    #read_doc_benchmark()
    #overall_benchmark()
