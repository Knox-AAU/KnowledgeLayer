from word_count import WordFrequencyHandler
from doc_classification import *
from api import ImportApi
from knox_source_data_io.io_handler import IOHandler, Generator
import uvicorn

def pipeline():
    print("Beginning of Knowledge Layer!")

    word_counter = WordFrequencyHandler()

    #while True:
    # TODO: Await API "call"
    uvicorn.run(ImportApi.app)
    temp_data = {"type": "Schema_Manual"}

    # Classify documents and call appropriate pre-processor
    document = DocumentClassifier.classify(temp_data)

    # TODO: Lemmatization of some form

    # TODO: Word count

    word_counter.do_word_count_for_article("DOCTITLE", "TEXT_BODY", ["PathList"])
    try:
        print(str(word_counter.get_next_pending_wordcount()))
    except IndexError:
        print("No elements")
    # Word counts can then be accessed with: word_counter[DOCTITLE][TERM]

    # TODO: (Out of scope for now) Construct knowledge graph depending on document type

    # TODO: Upload to database

    print("End of Knowledge Layer!")


if __name__ == "__main__":
    pipeline()
