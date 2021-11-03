import datetime
import logging

from pre_processing import PreProcessor
from publication_generator import PublicationGenerator
from performace_test_suite import PerformanceTestSuite

logger = logging.getLogger()

def run_tests():
    temp = 0
    generator = PublicationGenerator("NJ")
    generator.repeat_amount = 20
    generator.stop_word_density = 0
    generator.paragraph_word_count = temp
    preprocessor = PreProcessor()
    suite = PerformanceTestSuite(preprocessor.lemmatize, generator.publication_generator())
    #suite.setup_suite_func = lambda: mock_endpoint_thread.start()
    with open(f'test_{datetime.datetime.now().date()}_2.txt', "a") as f:
        f.write(str(suite.run()))


if __name__ == "__main__":
    run_tests()