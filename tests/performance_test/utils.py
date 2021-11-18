from tests.performance_test.publication_generator import PublicationGenerator


def make_generator(paragraph_amount, word_count, stop_dens):
    generator = PublicationGenerator("NJ")
    generator.repeat_amount = 5
    generator.stop_word_density = stop_dens / 10
    generator.article_amount = 2
    generator.paragraph_amount = paragraph_amount
    generator.paragraph_word_count = word_count
    return generator