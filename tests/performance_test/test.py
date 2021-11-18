
import os
from environment import EnvironmentVariables as Ev
from performance_overall import overall_benchmark
from performance_stop_words import stop_word_benchmark
from performance_word_counter import word_counter_benchmark
from performance_validate_json import validate_json_benchmark
from performance_lemma_api import run_tests as lemma_api_run_tests
from performance_lemma_internal import run_tests as lemma_internal_run_tests
from performance_moderndanish import run_tests as moderndanish_tests
Ev()

if __name__ == "__main__":
    path = Ev.instance.get_value(Ev.instance.PERFORMANCE_OUTPUT_FOLDER)
    if os.path.isdir(path) is False:
        os.mkdir(path)

    stop_word_benchmark()
    word_counter_benchmark()
    validate_json_benchmark()
    lemma_api_run_tests()
    lemma_internal_run_tests()
    moderndanish_tests()
    overall_benchmark()
