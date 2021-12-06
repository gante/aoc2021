""" Random utilities """

import time
from datetime import timedelta
from functools import wraps
from typing import Callable, Tuple


def measure_time(function: Callable):
    """ Decorator to print execution time of a function """

    @wraps(function)
    def decorated() -> Tuple[int, int, timedelta]:
        start = time.time()
        results = function()
        end = time.time()
        duration = timedelta(seconds=end-start)
        return (results[0], results[1], duration)

    return decorated


def print_results(problem_1: int, problem_2: int, duration: timedelta):
    """ Prints the solutions to the problem"""
    print(f"Solution to part 1: {problem_1}")
    print(f"Solution to part 2: {problem_2}")
    print(f"Compute duration: {duration}")
