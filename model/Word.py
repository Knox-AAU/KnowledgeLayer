from dataclasses import dataclass


@dataclass
class Word:
    """
    Contains a word and the amount of appearances
    """
    word: str
    amount: str
