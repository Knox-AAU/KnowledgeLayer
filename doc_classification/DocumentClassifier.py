import logging
from model.Document import Document, Article
from pre_processing import *

logging.basicConfig(
    format='%(asctime) | %(message)',
    datefmt='%Y %m %d @ %H:%M:%S'
)

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

class DocumentClassifier:
    """
    A module that classifies JSON data depending on the "type" attribute from the schema, and calls the
    appropriate pre-processing module.

    Ex. Data with type "Schema_Manual" is classified as Grundfos data and is passed to the GFPreProcessor for
    further pre-processing.
    """

    def __init__(self):
        self.nj_preprocessor = NJPreProcessor()
        self.gf_preprocessor = GFPreProcessor("en_core_web_sm")

    def classify(self, document_dict):
        """
        Classifies the JSON data according to its data source and calls the appropriate pre-processor.

        :param document_dict: Dictionary containing document information
        :return: Document object containing document title, body, publisher, and path
        """

        # Construct Document object from document_dict
        publisher = document_dict["content"]["publisher"]
        document = Document(publisher)
        total_number_of_articles = len(document_dict["content"]["articles"])
        total_number_of_processed_articles = 0

        for article in document_dict["content"]["articles"]:
            logger.info(f"Preprocces {publisher} - {int(total_number_of_articles/total_number_of_processed_articles)}%")
            title = article["headline"]
            # TODO: Why is extracted_from a list? Figure this out
            path = article["extracted_from"][0]
            body = ""

            for paragraph in article["paragraphs"]:
                body += ' ' + paragraph["value"]

            article = Article(title, body, path)
            document.articles.append(article)

        logger.info(f"Preprocces {document.publisher} - 100%")
        if document_dict["type"] == "Publication":
            logger.info(f"NJPreprocces {document.publisher} - 0%")
            processed_document = self.nj_preprocessor.process(document)
        elif document_dict["generator"]["app"] == "GrundfosManuals_Handler":
            logger.info(f"GFPreprocces {document.publisher} - 0%")
            processed_document = self.gf_preprocessor.process(document)
        else:
            raise Exception("Unable to classify document")

        return processed_document

    @staticmethod
    def extract_doc_paths(doc):
        paths = []

        for article in doc["content"]["articles"]:
            if "extracted_from" in article:
                for path in article["extracted_from"]:
                    paths.append(path)

        return paths
