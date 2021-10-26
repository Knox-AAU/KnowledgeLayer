from model import Document


class PreProcessor:
    """

    """
    def lemmatize(self, text, language):
        """

        :return:
        """
        raise NotImplementedError

    def process(self, document: Document) -> Document:
        print("Not overridden")
