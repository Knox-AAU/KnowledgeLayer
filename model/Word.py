from dataclasses import dataclass


@dataclass
class Word:
    """
    Contains a word and the number of occurrences
    """
    word: str
    amount: str
