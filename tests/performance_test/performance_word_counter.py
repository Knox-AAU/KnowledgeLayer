import os
import uuid

from environment import EnvironmentVariables as Ev
from tests.performance_test.performace_test_suite import PerformanceTestCase
from tests.performance_test.publication_generator import PublicationGenerator
from word_count import WordCounter
import logging
logger = logging.getLogger()


def word_counter_benchmark():
    wc = WordCounter.count_words

    gen = PublicationGenerator("NJ")
    suite = PerformanceTestCase(wc, None)
    path = os.path.join(Ev.instance.get_value(Ev.instance.PERFORMANCE_OUTPUT_FOLDER),
                        f"test_word_counter_{uuid.uuid4()}.csv")
    with open(path, 'a') as f:
        f.write("word_amount;data\n")
        for word_amount in range(100, 1010, 10):
            gen.paragraph_word_count = word_amount
            suite.data_generator = [gen.generate_paragraph()['value']]
            f.write(f'{word_amount};{suite.run()}\n')