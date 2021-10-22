from model.Document import Document
from model.Word import Word


class WordCounter:

    @staticmethod
    def count_document(doc: Document):
        word_counts = {}

        for word in doc.body.split():
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

        words = []

        for word, count in word_counts.items():
            word = Word(word, count)
            words.append(word)

        return words
