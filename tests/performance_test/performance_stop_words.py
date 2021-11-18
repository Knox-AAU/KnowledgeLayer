import os
import uuid

from model.Document import Article
from pre_processing import NJPreProcessor
from tests.performance_test.performace_test_suite import PerformanceTestCase
from tests.performance_test.publication_generator import PublicationGenerator
from environment import EnvironmentVariables as Ev
import logging
logger = logging.getLogger()

Ev()


def stop_word_benchmark():
    remove_stop_words = NJPreProcessor().remove_stopwords
    suite = PerformanceTestCase(remove_stop_words, None)

    gen = PublicationGenerator("NJ")
    path = os.path.join(Ev.instance.get_value(Ev.instance.PERFORMANCE_OUTPUT_FOLDER),
                        f"test_stop_words_{uuid.uuid4()}.csv")
    with open(path, 'a') as f:
        f.write("word_amount;stop_word_dens;data\n")
        for word_amount in range(100, 1100, 100):
            for stop_word_dens in range(11):
                gen.paragraph_word_count = word_amount
                gen.stop_word_density = stop_word_dens/10
                suite.data_generator = [[Article("", gen.generate_paragraph()['value'],"")]]
                f.write(f'{word_amount};{stop_word_dens/10};{suite.run()}\n')