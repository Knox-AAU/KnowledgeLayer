import datetime
import logging

from model.Document import Article
from pre_processing import NJPreProcessor
from publication_generator import PublicationGenerator
from performace_test_suite import PerformanceTestSuite

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

            suite = PerformanceTestSuite(preprocessor.convert_to_modern_danish, argList)

            with open(f'test_{datetime.datetime.now().date()}_2.txt', "a") as f:
                f.write(str(numbParagraph) + ", " + str(numbWordcount) + ", " + str(suite.run()).replace("[", "").replace("]", "") + "\n")

            numbWordcount += 1000
        numbParagraph += 1


if __name__ == "__main__":
    run_tests()