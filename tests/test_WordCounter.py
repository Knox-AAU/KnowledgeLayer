import pytest

from word_count.WordCounter import WordCounter

xFail = pytest.mark.xfail


class Test:

    def test_sentence_one(self):
        # Arrange
        sentence = "can you please count correctly count me please please count me"

        # Act
        result = WordCounter.count_words(sentence)
        total_words = result[0]
        word_list = result[1]

        # Assert
        assert total_words == 11
        assert word_list[0].word == "can" and word_list[0].amount == 1
        assert word_list[1].word == "you" and word_list[1].amount == 1
        assert word_list[2].word == "please" and word_list[2].amount == 3
        assert word_list[3].word == "count" and word_list[3].amount == 3
        assert word_list[4].word == "correctly" and word_list[4].amount == 1
        assert word_list[5].word == "me" and word_list[5].amount == 2

    def test_sentence_two(self):
        # Arrange
        sentence = "two_zero c to seven_zero c four f to one_five_eight f factoryfille with antifreeze liquid"

        # Act
        result = WordCounter.count_words(sentence)
        total_words = result[0]
        word_list = result[1]

        # Assert
        assert total_words == 14
        assert word_list[0].word == "two_zero" and word_list[0].amount == 1
        assert word_list[1].word == "c" and word_list[1].amount == 2
        assert word_list[2].word == "to" and word_list[2].amount == 2
        assert word_list[3].word == "seven_zero" and word_list[3].amount == 1
        assert word_list[4].word == "four" and word_list[4].amount == 1
        assert word_list[5].word == "f" and word_list[5].amount == 2
        assert word_list[6].word == "one_five_eight" and word_list[6].amount == 1
        assert word_list[7].word == "factoryfille" and word_list[7].amount == 1
        assert word_list[8].word == "with" and word_list[8].amount == 1
        assert word_list[9].word == "antifreeze" and word_list[9].amount == 1
        assert word_list[10].word == "liquid" and word_list[10].amount == 1

    def test_empty_sentence(self):
        # Arrange
        sentence = ""

        # Act
        result = WordCounter.count_words(sentence)
        total_words = result[0]
        word_list = result[1]

        # Assert
        assert total_words == 0
        assert word_list == []
