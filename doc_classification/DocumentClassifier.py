from pre_processing import *


class DocumentClassifier:
    """
    A module that classifies JSON data depending on the "type" attribute from the schema, and calls the
    appropriate pre-processing module.

    Ex. Data with type "Schema_Manual" is classified as Grundfos data and is passed to the GFPreProcessor for
    further pre-processing.
    """
    @staticmethod
    def classify(json_data):
        """
        Classifies the JSON data according to its data source and calls the appropriate pre-processor
        :argument json_data Dictionary containing document information
        :return: Result of the appropriate pre-processing module
        """
        if json_data["type"] == "Schema_Article":
            nj_pre_proc = NJPreProcessor()
            return nj_pre_proc.process(json_data)
        elif json_data["type"] == "Schema_Manual":
            gf_pre_proc = GFPreProcessor("en_core_web_sm")
            return gf_pre_proc.process(json_data)
