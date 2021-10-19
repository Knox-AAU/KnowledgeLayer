from abc import abstractmethod


class PreProcessor:
    """

    """
    def lemmatize(self, text):
        """

        :return:
        """
        # TODO: Call lemmatization API here
        raise NotImplementedError

    #@abstractmethod
    def process(self, json_data):
        pass
