import datetime
import logging
import os
import uuid

from model.Document import Article
from pre_processing import NJPreProcessor
from publication_generator import PublicationGenerator
from performace_test_suite import PerformanceTestCase
from environment import EnvironmentVariables as Ev
Ev()
logger = logging.getLogger()

def run_tests():
    numbWordcount = 1000
    numbParagraph = 1
    numbIterations = 10

    generator = PublicationGenerator("NJ")
    generator.repeat_amount = numbIterations
    generator.stop_word_density = 0
    generator.paragraph_word_count = numbWordcount
    generator.paragraph_amount = numbParagraph
    preprocessor = NJPreProcessor()

    for j in range(10):
        generator.paragraph_amount = numbParagraph
        for k in range(10):
            generator.paragraph_word_count = numbWordcount
            argList = []

            #generate list
            for i in range(numbIterations):
                generatedArticle = generator.generate_article()
                articleBody = ""
                for paragraph in generatedArticle["paragraphs"]:
                    articleBody += " " + paragraph["value"]
                newArticle = Article(generatedArticle['headline'], articleBody, generatedArticle['extracted_from'][0])
                argList.append([newArticle])

            suite = PerformanceTestCase(preprocessor.convert_to_modern_danish, argList)

            path = os.path.join(Ev.instance.get_value(Ev.instance.PERFORMANCE_OUTPUT_FOLDER),
                                f"test_moderndanish_{uuid.uuid4()}.csv")
            with open(path, 'a') as f:
                f.write(str(numbParagraph) + ", " + str(numbWordcount)
                        + ", " + str(suite.run()).replace("[", "").replace("]", "") + "\n")

            numbWordcount += 1000
        numbParagraph += 1


if __name__ == "__main__":
    run_tests()