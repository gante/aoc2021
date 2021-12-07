""" Solution to day 07

Lessons from the problem:
-
"""

import os
from typing import Tuple

import numpy as np
import numpy.typing as npt

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def min_fuel_to_align_1(crab_positions: npt.NDArray) -> int:
    """
    Finds and returns the minimum fuel required to align the crabs (linear fuel cost)

    This problem is essentially minimising the L1 distance, whose optimal value is given by the
    median of the distribution.
    """
    median_position = np.round(np.median(crab_positions))
    fuel = np.abs(crab_positions - median_position)
    return int(np.sum(fuel))


def min_fuel_to_align_2(crab_positions: npt.NDArray) -> int:
    """ Finds and returns the minimum fuel required to align the crabs (increasing fuel cost)

    Q: why does `np.floor(np.mean(crab_positions))` gives us the optimal position here?
    """

    def compute_fuel(x: int) -> int:
        distance = np.abs(crab_positions - x)
        fuels = (distance * (distance + 1)) / 2
        return int(np.sum(fuels))

    opt_position = np.floor(np.mean(crab_positions))
    return compute_fuel(opt_position)


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    with open(os.path.join(DATA_PATH, "day_07.txt")) as input_file:
        for line in input_file:
            line = line.rstrip('\n')
            crab_positions_input = [int(pos) for pos in line.split(",")]

    crab_positions = np.asarray(crab_positions_input)
    problem_1 = min_fuel_to_align_1(crab_positions)
    problem_2 = min_fuel_to_align_2(crab_positions)
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
