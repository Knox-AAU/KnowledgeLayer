from word_count.TermFrequency import TermFrequency

def pipeline():
    print("Beginning of Knowledge Layer!")

    word_counter = TermFrequency()

    #while True:
    # TODO: Await API "call"

    # TODO: Classify documents
    # Call appropriate preprocessor depending on document type

    # TODO: Lemmatization of some form

    # TODO: Word count
    word_counter.process("DOCTITLE", "TEXT_BODY")
    # Word counts can then be accessed with: word_counter[DOCTITLE][TERM]

    # TODO: (Out of scope for now) Construct knowledge graph depending on document type

    # TODO: Upload to database

    print("End of Knowledge Layer!")

if __name__ == "__main__":
    pipeline()