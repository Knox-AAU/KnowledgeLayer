from word_count import WordFrequencyHandler
from doc_classification import *
# from environment import *
from environment import EnvironmentVariables as Ev


def pipeline():
    print("Beginning of Knowledge Layer!")

    # Instantiate EnvironmentVariables class for future use. Environment constants cannot be accessed without this
    Ev()

    word_counter = WordFrequencyHandler()

    # while True:
    # TODO: Await API "call"
    temp_data = {"type": "Schema_Manual"}

    # Classify documents and call appropriate pre-processor
    document = DocumentClassifier.classify(temp_data)

    # TODO: Lemmatization of some form

    # TODO: Word count

    word_counter.word_count_document("DOCTITLE", "Count this sentence", ["Path"])
    try:
        print(str(word_counter.get_next_pending_wordcount()))
    except IndexError:
        print("No elements")

    # TODO: (Out of scope for now) Construct knowledge graph depending on document type

    # TODO: Upload to database

    print("End of Knowledge Layer!")


if __name__ == "__main__":
    pipeline()
