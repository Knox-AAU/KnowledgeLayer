from dataclasses import dataclass
from typing import List
from model.Word import Word


@dataclass
class DocumentWordCountDto:
    """
    Data transfer object for the word count result of a document. Adheres to the /WordCount endpoint JSON schema. See
    the Knox wiki page.
    """
    articletitle: str
    filepath: str
    totalwordsinarticle: int
    words: List[Word]
    publication: str
