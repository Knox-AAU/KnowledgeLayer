from typing import Optional, Any, Iterator, Callable, List

import time
import logging

logger = logging.getLogger()


class PerformanceTestSuite:
    def __init__(self, target: Callable[[Any], Any], arg_generator: Iterator):
        self.target = target
        self.data_generator = arg_generator
        self.setup_suite_func: Optional[Callable[[], Any]] = None
        self.setup_test_func: Optional[Callable[[], Any]] = None
        self.shutdown_suite_func: Optional[Callable[[], Any]] = None
        self.shutdown_test_func: Optional[Callable[[], Any]] = None

    def run(self):
        result = []
        logger.warning("\n------SETTING UP SUITE------")
        if self.setup_suite_func is not None:
            self.setup_suite_func()

        logger.warning("\n------STARTING TESTING------")
        for index, data in enumerate(self.data_generator):

            if self.setup_test_func is not None:
                logger.warning(f"\n------SETTING UP TEST {index}------")
                self.setup_test_func()
            logger.warning(f"\n------RUNNING TEST {index}------")
            result.append(self.__run_test(data))
            if self.shutdown_test_func is not None:
                logger.warning(f"\n------SHUTTING DOWN TEST {index}------")
                self.shutdown_test_func()

        if self.shutdown_suite_func is not None:
            logger.warning("\n------SHUTTING DOWN SUITE------")
            self.shutdown_suite_func()

        return result

    def setup_test(self, func: Optional[Callable[[], Any]]):
        self.setup_test_func = func

    def setup_suite(self, func: Optional[Callable[[], Any]]):
        self.setup_suite_func = func

    def shutdown_test(self, func: Optional[Callable[[], Any]]):
        self.shutdown_test_func = func

    def shutdown_suite(self, func: Optional[Callable[[], Any]]):
        self.shutdown_suite_func = func

    def __run_test(self, data: [Any]):
        t1 = time.time()
        self.target(*data)
        t2 = time.time()
        return t2 - t1
