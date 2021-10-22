
from dataclasses import dataclass
from typing import List

from word_count.WordFrequencyHandler import Word


@dataclass
class DocumentWordCountDto:
    """

    """
    articletitle: str
    filepath: str
    totalwordsinarticle: int
    words: List[Word]
    publication: str
