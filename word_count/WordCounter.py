from model.Word import Word


class WordCounter:

    @staticmethod
    def count_words(text: str):
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
