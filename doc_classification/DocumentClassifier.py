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
        doc_title = document_dict["content"]["title"]
        doc_publisher = document_dict["content"]["publisher"]
        # TODO: Insert correct field when this is known
        doc_path = "TEMP_PATH"

        document = Document(doc_title, doc_publisher, doc_path)

        if document_dict["type"] == "Schema_Article":
            nj_pre_proc = NJPreProcessor()
            document.body = nj_pre_proc.process(document_dict)
        elif document_dict["type"] == "Schema_Manual":
            gf_pre_proc = GFPreProcessor("en_core_web_sm")
            document.body = gf_pre_proc.process(document_dict)

        return document


class Document:
    def __init__(self, title, publisher, path):
        self.title = title
        self.publisher = publisher
        self.path = path
        self.body = ""
