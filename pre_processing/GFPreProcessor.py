import spacy
import re
from pre_processing.PreProcessor import PreProcessor


class GFPreProcessor(PreProcessor):
    """

    """
    def __init__(self, model):
        self.nlp = spacy.load(model)

    def process(self, json_data):
        """

        :return:
        """

        # corpus = self.extract_all_text_from_paragraphs(json_data)
        # corpus = self.remove_special_characters(corpus)
        # corpus = self.numbers_to_text(corpus)
        # # corpus = super().lemmatize(corpus)
        # corpus = self.bigrams(corpus)
        # corpus = self.to_lower(corpus)

        # TODO: Do actual processing
        corpus = "I am a testing sentence or something"

        return corpus

    def extract_all_text_from_paragraphs(self, data):
        """

        :param data:
        :return:
        """
        # TODO: Implement this method
        raise NotImplementedError

    # TODO: Review all methods below and ensure that they are relevant and correct

    def bigrams(self, sentence: str) -> str:
        """

        :param sentence:
        :return:
        """
        doc = self.nlp(sentence)

        for noun_phrase in list(doc.noun_chunks):
            if noun_phrase.string.endswith(' '):
                bigram = noun_phrase.string
                # Remove trailing whitespace in noun_phrase to avoid:
                # "ice cream " --> "ice_cream_"
                # Instead of "ice cream " --> "ice_cream "
                bigram = bigram.strip(' ')
                bigram = bigram.replace(' ', '_')
                bigram += ' '
            else:
                bigram = noun_phrase.string
                bigram = bigram.strip(' ')
                bigram = bigram.replace(' ', '_')

            sentence = sentence.replace(noun_phrase.string, bigram)

        return sentence

    def to_lower(self, words):
        """

        :param words:
        :return:
        """
        return words.lower()

    def remove_special_characters(self, txt):
        """

        :param txt:
        :return:
        """
        cleaned_text = re.sub("[^a-zA-Z. ]", '', txt)
        return cleaned_text

    def numbers_to_text(self, text):
        """

        :param text:
        :return:
        """
        result = ""

        for token in text.split():
            if token.isdigit():
                result += self._textify_token(token)
            else:
                result += token
            result += " "

        return result.strip()

    def _textify_token(self, token):
        """

        :param token:
        :return:
        """
        result = ""
        for digit in token:
            result += self._textify_number(digit)
            result += " "

        return result.strip()

    def _textify_number(self, digit):
        """

        :param digit:
        :return:
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
        return numbers[digit]

    def remove_duplicates(self, str_list):
        """

        :return:
        """
        return list(set(str_list))


#    def insert_pump_name(self, data, pump_name):
#        data = data.replace("the_pump", pump_name)
#        return data
