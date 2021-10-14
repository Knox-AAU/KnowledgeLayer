from pre_processing.PreProcessor import PreProcessor

class NJPreProcessor(PreProcessor):
    """

    """
    def __init__(self, model):
        super().__init__(model)
        self.nlp = spacy.load(self.spacyModel)

    def process(self, json_data):
        """

        :return:
        """
        # TODO: Do actual processing
        return json_data
