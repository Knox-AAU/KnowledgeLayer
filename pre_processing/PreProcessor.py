from abc import ABC, abstractmethod


class PreProcessor(ABC):
    """

    """
    def lemmatize(self):
        """

        :return:
        """
        # TODO: Call lemmatization API here
        raise NotImplementedError

    @abstractmethod
    def process(self, json_data):
        pass
