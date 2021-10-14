import threading

from word_count import WordFrequencyHandler
from doc_classification import *
from api import ImportApi
import uvicorn

def runApi():
    uvicorn.run(ImportApi.app)

def pipeline():
    print("Beginning of Knowledge Layer!")

    word_counter = WordFrequencyHandler()

    #while True:
    # TODO: Await API "call"
    #Start a seperate thread for the API to avoid blocking
    api_thread = threading.Thread(target=runApi)
    api_thread.start()

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
