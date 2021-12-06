""" Solution to day 03

Lessons from the problem:
- Casting to int on a bit per bit basis (`[int(bit) for bit in line]`) is expensive (~3ms) relative
to the rest of the code. List comprehensions are still prefered over `map` for the core devs.
(https://stackoverflow.com/questions/1247486/list-comprehension-vs-map#comment1074551_1247490)
"""

import os
from typing import Tuple

import numpy as np
import numpy.typing as npt

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def binary_to_numeric(binary_number: npt.NDArray) -> int:
    """ Returns the numeric (base 10) correspondent of a binary number """
    return int(sum([2**(idx) for idx, bit in enumerate(binary_number[::-1]) if bit > 0.]))


def get_gamma_epsilon(binary_array: npt.NDArray) -> Tuple[int, int]:
    """ Given the binary array, gets gamma and epsilon (in a numerical format) """
    averages = np.mean(binary_array, axis=0)
    gamma_binary = np.round(averages)
    epsilon_binary = 1 - gamma_binary
    gamma = binary_to_numeric(gamma_binary)
    epsilon = binary_to_numeric(epsilon_binary)
    return gamma, epsilon


def get_oxigen_co2(binary_array: npt.NDArray) -> Tuple[int, int]:
    """
    Given the binary array, gets the oxigen generator and CO2 scrubber ratings (in a numerical
    format)
    """
    # oxigen
    oxigen_binary_array = np.copy(binary_array)
    for idx in range(oxigen_binary_array.shape[1]):
        if oxigen_binary_array.shape[0] == 1:
            break
        bit = np.round(np.mean(oxigen_binary_array, axis=0)[idx] + 0.00001)
        oxigen_binary_array = oxigen_binary_array[oxigen_binary_array[:, idx] == bit]
    oxigen = binary_to_numeric(oxigen_binary_array[0])

    # co2
    co2_binary_array = np.copy(binary_array)
    for idx in range(co2_binary_array.shape[1]):
        if co2_binary_array.shape[0] == 1:
            break
        bit = 1 - np.round((np.mean(co2_binary_array, axis=0)[idx]) + 0.00001)
        co2_binary_array = co2_binary_array[co2_binary_array[:, idx] == bit]
    co2 = binary_to_numeric(co2_binary_array[0])

    return oxigen, co2


@measure_time
def get_solution():
    """ Solution to the problem """
    binary_list = []
    with open(os.path.join(DATA_PATH, "day_03.txt")) as input_file:
        for line in input_file:
            line = line.rstrip('\n')
            binary_list.append([int(bit) for bit in line])

    binary_array = np.asarray(binary_list)
    gamma, epsilon = get_gamma_epsilon(binary_array)
    problem_1 = gamma * epsilon
    oxigen, co2 = get_oxigen_co2(binary_array)
    problem_2 = oxigen * co2
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
