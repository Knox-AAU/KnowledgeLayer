import os

import spacy


def load_model(model: str, *args, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "..", model)
    return spacy.load(path, *args, **kwargs)
