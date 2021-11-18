import datetime
import logging

from pre_processing import PreProcessor
from publication_generator import PublicationGenerator
from performace_test_suite import PerformanceTestSuite

logger = logging.getLogger()

def run_tests():
    numbWordcount = 1000
    numbIterations = 10

    generator = PublicationGenerator("NJ")
    generator.repeat_amount = numbIterations
    generator.stop_word_density = 0
    generator.paragraph_word_count = numbWordcount
    preprocessor = PreProcessor()


    while numbWordcount <= 1000:
        generator.paragraph_word_count = numbWordcount
        argList = []

        #generate list
        for i in range(numbIterations):
            argList.append([generator.generate_paragraph()['value'], "da"])

        suite = PerformanceTestSuite(preprocessor.lemmatize, argList)
        #suite.setup_suite_func = lambda: mock_endpoint_thread.start()
        with open(f'test_{datetime.datetime.now().date()}_2.txt', "a") as f:
            f.write(str(numbWordcount) + ", " + str(suite.run()).replace("[", "").replace("]", "") + "\n")

        numbWordcount += 1000


if __name__ == "__main__":
    run_tests()
