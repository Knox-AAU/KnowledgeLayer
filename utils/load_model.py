import os

import spacy


def load_model(model: str, *args, **kwargs):
    """
    Loads the specified spaCy model.

    :param model: The name/path of the model to load
    :param args: Arguments for the model to load
    :param kwargs: ???
    :return: The loaded model
    """
    path = os.path.join(os.path.dirname(__file__), "..", model)
    return spacy.load(path, *args, **kwargs)
