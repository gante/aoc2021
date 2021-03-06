""" Solution to day 01

Lessons from the problem:
- Casting array to numpy makes things faster
"""

import os
from typing import Tuple

import numpy as np
import numpy.typing as npt

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def count_increases(depth_array: npt.NDArray, window_size: int) -> int:
    """ Returns how many times the value in the window is bigger than its predecessor """
    window_conv = np.asarray([1] * window_size)
    window_values = np.convolve(depth_array, window_conv, mode='valid')
    pred = window_values[:-1]
    succ = window_values[1:]
    diff = succ - pred
    return int(np.sum(np.where(diff > 0, 1, 0)))


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    depth_list = []
    with open(os.path.join(DATA_PATH, "day_01.txt")) as input_file:
        for line in input_file:
            line.strip()
            depth_list.append(int(line))

    depth_array = np.asarray(depth_list)
    problem_1 = count_increases(depth_array=depth_array, window_size=1)
    problem_2 = count_increases(depth_array=depth_array, window_size=3)
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
