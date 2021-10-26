from model.Document import Document, Article
from pre_processing import *


class DocumentClassifier:
    """
    A module that classifies JSON data depending on the "type" attribute from the schema, and calls the
    appropriate pre-processing module.

    Ex. Data with type "Schema_Manual" is classified as Grundfos data and is passed to the GFPreProcessor for
    further pre-processing.
    """
    @staticmethod
    def classify(document_dict):
        """
        Classifies the JSON data according to its data source and calls the appropriate pre-processor.

        :param document_dict: Dictionary containing document information
        :return: Document object containing document title, body, publisher, and path
        """

        # Construct Document object from document_dict
        publisher = document_dict["content"]["publisher"]
        document = Document(publisher)

        for article in document_dict["content"]["articles"]:
            title = article["headline"]
            # TODO: Why is extracted_from a list? Figure this out
            path = article["extracted_from"][0]
            body = ""

            for paragraph in article["paragraphs"]:
                body += paragraph["value"]

            article = Article(title, body, path)
            document.articles.append(article)

        if document_dict["type"] == "Schema_Article":
            nj_pre_proc = NJPreProcessor()
            processed_document = nj_pre_proc.process(document)
        elif document_dict["type"] == "Schema_Manual":
            gf_pre_proc = GFPreProcessor("en_core_web_sm")
            processed_document = gf_pre_proc.process(document)
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
