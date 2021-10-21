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

        corpus = super().extract_all_text_from_paragraphs(json_data)

        # TODO: Decide what to do with emails, links, etc. in corpus
        corpus = self.remove_special_characters(corpus)
        corpus = self.numbers_to_text(corpus)
        corpus = super().lemmatize(corpus)
        # corpus = self.bigrams(corpus)
        corpus = self.to_lower(corpus)

        return corpus

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
        cleaned_text = re.sub("[^a-zA-Z0-9 ]", '', txt)
        return cleaned_text

    # TODO: Consider researching string builders for this
    def numbers_to_text(self, text):
        """

        :param text:
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
