import json
import os
import uuid

from knox_source_data_io.io_handler import IOHandler

from tests.performance_test.performace_test_suite import PerformanceTestCase
from tests.performance_test.publication_generator import PublicationGenerator
from environment import EnvironmentVariables as Ev
import logging
logger = logging.getLogger()
Ev()


def validate_json_benchmark():
    schema_path = os.path.dirname(os.path.abspath(__file__))
    test_func = lambda json: IOHandler.validate_json(json, os.path.join(schema_path, '../..', 'schema.json'))
    suite = PerformanceTestCase(test_func, None)
    path = os.path.join(Ev.instance.get_value(Ev.instance.PERFORMANCE_OUTPUT_FOLDER),
                        f"test_read_doc_{uuid.uuid4()}.csv")
    generator = PublicationGenerator("NJ", paragraph_amount=1,
                                     article_amount=1, paragraph_word_count=10)
    with open(os.path.join(Ev.instance.get_value(Ev.instance.PERFORMANCE_OUTPUT_FOLDER), f"example_output.txt"), 'a') as f:
        f.write(json.dumps(next(generator.publication_generator())))
    with open(path, 'a') as f:
        f.write("paragraph_amount;article_amount;data\n")
        for paragraph_amount in range(1, 11):
            for article_amount in range(1, 11):
                generator = PublicationGenerator("NJ", paragraph_amount=paragraph_amount,
                                                 article_amount=article_amount, paragraph_word_count=10)
                generator.set_seed(paragraph_amount + article_amount)
                suite.data_generator = pub_gen(generator.publication_generator())
                f.write(f'{paragraph_amount};{article_amount};{suite.run()}\n')

def pub_gen(gen):
    yield gen