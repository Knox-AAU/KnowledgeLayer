import datetime
import logging
import os
import uuid

from pre_processing import PreProcessor
from publication_generator import PublicationGenerator
from performace_test_suite import PerformanceTestCase
from environment import EnvironmentVariables as Ev

Ev()
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

        # generate list
        for i in range(numbIterations):
            argList.append([generator.generate_paragraph()['value'], "da"])

        suite = PerformanceTestCase(preprocessor.lemmatize, argList)
        path = os.path.join(Ev.instance.get_value(Ev.instance.PERFORMANCE_OUTPUT_FOLDER),
                            f"test_word_counter_{uuid.uuid4()}.csv")
        with open(path, 'a') as f:
            f.write(str(numbWordcount) + ", " + str(suite.run()).replace("[", "").replace("]", "") + "\n")

        numbWordcount += 1000


if __name__ == "__main__":
    run_tests()
