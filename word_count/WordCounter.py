from model.Word import Word


class WordCounter:
    """
    The class responsible for counting word occurrences in an article, as well as keeping track of the total number
    of words in the article.
    """

    @staticmethod
    def count_words(text: str):
        """
        Counts the word occurrences of each word in the input text, as well as the total number of words.

        :param text: The string to have words counted
        :return: A tuple containing the total number of words, as well as a list of occurrences for each word
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
