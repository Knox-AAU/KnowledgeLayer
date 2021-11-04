from model.Word import Word


class WordCounter:
    """
    Component responsible for all word counting
    """

    @staticmethod
    def count_words(text: str):
        """
        :param text: text of words. It is assumed to be preprocessed
        :return: returns a tuple with the first element being the total count of words, and the second element
        being a list of Word objects containing the name of the word and the amount of times it appears in the text.
        """
        word_counts = {}

        words = text.split()
        total_words = len(words)

        for word in words:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

        word_count_list = []

        for word, count in word_counts.items():
            word = Word(word, count)
            word_count_list.append(word)

        return total_words, word_count_list
