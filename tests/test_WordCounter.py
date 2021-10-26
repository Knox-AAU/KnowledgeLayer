import pytest

from word_count.WordCounter import WordCounter

xFail = pytest.mark.xfail


class Test:

    def test_sentence_one(self):
        # arrange
        sentence = "can you please count correctly count me please please count me"

        # act
        result = WordCounter.count_words(sentence)
        total_words = result[0]
        word_list = result[1]

        # assert
        assert total_words == 11
        assert word_list[0].word == "can" and word_list[0].amount == 1
        assert word_list[1].word == "you" and word_list[1].amount == 1
        assert word_list[2].word == "please" and word_list[2].amount == 3
        assert word_list[3].word == "count" and word_list[3].amount == 3
        assert word_list[4].word == "correctly" and word_list[4].amount == 1
        assert word_list[5].word == "me" and word_list[5].amount == 2
