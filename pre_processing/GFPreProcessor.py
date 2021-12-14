from utils import logging
import re
from pre_processing.PreProcessor import PreProcessor


class GFPreProcessor(PreProcessor):
    """
    The pre-processing module for Grundfos data.
    This pre-processing handles converting article bodies and titles to lowercase, removing special characters,
    and converting numbers to text.
    """

    def process(self, document):
        """
        This method handles the overall pre-processing of a Document object, by iterating through every article in it
        and calling the appropriate processing methods.

        :param document: The Document object encapsulating information from the input to the pipeline
        :return: A Document object containing the pre-processed body
        """
        total_number_of_articles = len(document.articles)
        total_number_of_processed_articles = 0

        for article in document.articles:
            logging.LogF.log(
                f"{int((total_number_of_processed_articles * 100) / total_number_of_articles)}% : GFPreProcessing of {document.publisher} - {article.title}")
            article.title = self.__process_text__(document, article.title)
            article.body = self.__process_text__(document, article.body)
            total_number_of_processed_articles += 1

        logging.LogF.log(f"100% : GFPreProcessing of {document.publisher}")

        return document

    def __process_text__(self, document, text: str):
        """
        Calls the various processing methods for the input text (either an article title, or body).

        :param document: The Document object (only used for logging)
        :param text: The body of the article to process
        :return: The pre-processed body of one article as a string
        """
        # TODO: Decide what to do with emails, links, etc. in corpus
        corpus = self.remove_special_characters(text)
        corpus = self.numbers_to_text(corpus)
        logging.LogF.log(f"Call Lemmatization for {document.publisher}")
        corpus = super().lemmatize(corpus, "en")
        logging.LogF.log(f"Response from Lemmatization for {document.publisher}")
        return self.to_lower(corpus)

    def bigrams(self, sentence: str) -> str:
        # This is an experiment! Can be the basis for greatness later on

        # self.nlp.add_pipe("merge_noun_chunks")
        #
        # doc = self.nlp(corpus)
        # print("spaCy text: " + doc.text)
        # for chunk in list(doc.noun_chunks):
        #     print(chunk)
        #
        # for token in doc:
        #     print(token.text + ", " + token.pos_)
        return True

    def to_lower(self, text):
        """
        Converts the input text to lowercase.

        :param text: The body (or title) of one article
        :return: The input text in lowercase
        """
        return text.lower()

    def remove_special_characters(self, text):
        """
        Removes all characters from the input text that aren't a-z, A-Z, 0-9, or spaces.

        :param text: The text to have special characters removed from
        :return: The input text with special characters removed
        """
        cleaned_text = re.sub("[^a-zA-Z0-9 ]", '', text)
        return cleaned_text

    # TODO: Consider researching string builders for this
    def numbers_to_text(self, text):
        """
        Converts occurrences of numbers into a textual format.

        Ex. 9 becomes nine, and 56 becomes five_six.

        :param text: The text to convert numbers to text in
        :return: The input text with numbers converted to textual format
        """
        numbers = {
            '0': 'zero',
            '1': 'one',
            '2': 'two',
            '3': 'three',
            '4': 'four',
            '5': 'five',
            '6': 'six',
            '7': 'seven',
            '8': 'eight',
            '9': 'nine'
        }

        result = ""
        just_seen_digit = False

        for character in text:
            if character.isnumeric():
                if just_seen_digit:
                    result += "_"
                result += numbers[character]
                just_seen_digit = True
            else:
                result += character
                just_seen_digit = False

        return result.strip()

#    def insert_pump_name(self, data, pump_name):
#        data = data.replace("the_pump", pump_name)
#        return data
