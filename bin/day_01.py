""" Solution to day 01

Lessons from the problem:
-
"""

import os
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def count_increases(depth_list, window_size):
    """ Returns how many times the value in the window is bigger than its predecessor """
    window_conv = np.asarray([1] * window_size)
    window_values = np.convolve(depth_list, window_conv, mode='valid')
    pred = window_values[:-1]
    succ = window_values[1:]
    diff = succ - pred
    return np.sum(np.where(diff > 0, 1, 0))


def get_solution():
    """ Solution to the problem """
    depth_list = []
    with open(os.path.join(DATA_PATH, "day_01.txt")) as input_file:
        for line in input_file:
            line.strip()
            depth_list.append(int(line))

    problem_1 = count_increases(depth_list=np.asarray(depth_list), window_size=1)
    problem_2 = count_increases(depth_list=np.asarray(depth_list), window_size=3)
    return problem_1, problem_2


if __name__ == "__main__":
    result_1, result_2 = get_solution()
    print(f"Solution to part 1: {result_1}")
    print(f"Solution to part 2: {result_2}")
