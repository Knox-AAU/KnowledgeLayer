import os
import uuid
from unittest.mock import patch

from doc_classification import PipelineManager
from tests.performance_test.performace_test_suite import PerformanceTestCase
from tests.performance_test.publication_generator import PublicationGenerator

from tests.performance_test.utils import make_generator
from environment import EnvironmentVariables as Ev
import logging
logger = logging.getLogger()

Ev()

@patch('data_access.WordCountDao.send_word_count')
@patch('pre_processing.PreProcessor.lemmatize')
def overall_benchmark(mock_lemma, mock_send_word):
    # benchmark on processStoredPublications()
    pipeline = PipelineManager()
    mock_lemma.side_effect = lambda x, y: x
    mock_send_word.return_value = None
    suite = PerformanceTestCase(pipeline.processStoredPublications, make_generator(0, 0, 0).publication_generator())

    generator = PublicationGenerator("NJ")
    generator.repeat_amount = 1
    generator.article_amount = 1
    path = os.path.join(Ev.instance.get_value(Ev.instance.PERFORMANCE_OUTPUT_FOLDER),
                        f"test_overall_{uuid.uuid4()}.csv")
    with open(path, 'a') as f:
        f.write("paragraph_amount;word_count;stop_dens;data\n")
        for paragraph_amount in range(1, 11):
            for word_count in range(100, 1100, 100):
                for stop_dens in range(11):
                    generator.stop_word_density = stop_dens / 10
                    generator.paragraph_amount = paragraph_amount
                    generator.paragraph_word_count = word_count
                    generator.set_seed(paragraph_amount + word_count + stop_dens)
                    suite.data_generator = pub_gen(generator.publication_generator())
                    f.write(f'{paragraph_amount};{word_count};{stop_dens};{suite.run()}\n')
                    logger.warning(f'{paragraph_amount};{word_count};{stop_dens};{suite.run()}\n')

    #
    # wordcount = generator.article_amount * generator.paragraph_amount * generator.paragraph_word_count
    # data = suite.run()
    # import numpy as np
    # print(((len(data) - 1) * wordcount) / np.array(data[1:]).sum())
    gen = PublicationGenerator("NJ")
    data = []
    for i in range(100, 1100, 100):
        gen.paragraph_word_count = i
        data.append(gen.__get_random_sentence())

def pub_gen(gen):
    yield gen