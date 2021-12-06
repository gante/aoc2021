""" Solution to day 05

Lessons from the problem:
- numpy slicing is pretty damn fast
- 2D slicing in numpy doesn't need stacked slices
"""

import os
from typing import Tuple

import numpy as np
import numpy.typing as npt

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def get_danger_map(coordinate_tensor: npt.NDArray, use_diagonals: bool) -> npt.NDArray:
    """ Computes and returns the map containing the danger level of each coordinate """
    max_x = np.max(coordinate_tensor[:, :, 0])
    max_y = np.max(coordinate_tensor[:, :, 1])
    danger_map = np.zeros((max_x+1, max_y+1), dtype=int)
    for pair in coordinate_tensor:
        x_slice = np.linspace(
            start=pair[0, 0],
            stop=pair[1, 0],
            num=np.abs(pair[0, 0]-pair[1, 0])+1,
            dtype=int
        )
        y_slice = np.linspace(
            start=pair[0, 1],
            stop=pair[1, 1],
            num=np.abs(pair[0, 1]-pair[1, 1])+1,
            dtype=int
        )
        x_length = x_slice.size
        y_length = y_slice.size
        if (not use_diagonals) and x_length > 1 and y_length > 1:
            continue
        if x_length < y_length:
            assert x_length == 1
            x_slice = np.repeat(x_slice, y_length)
        elif x_length > y_length:
            assert y_length == 1
            y_slice = np.repeat(y_slice, x_length)
        danger_map[x_slice, y_slice] += 1
    return danger_map


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    coordinate_pairs = []
    with open(os.path.join(DATA_PATH, "day_05.txt")) as input_file:
        for line in input_file:
            line = line.rstrip('\n')
            pair_1, pair_2 = line.split(" -> ")
            pair_1_decoded = [int(pos) for pos in pair_1.split(",")]
            pair_2_decoded = [int(pos) for pos in pair_2.split(",")]
            coordinate_pairs.append([pair_1_decoded, pair_2_decoded])

    coordinate_tensor = np.asarray(coordinate_pairs)
    danger_map = get_danger_map(coordinate_tensor, use_diagonals=False)
    problem_1 = np.sum(np.where(danger_map > 1, 1, 0))
    danger_map = get_danger_map(coordinate_tensor, use_diagonals=True)
    problem_2 = np.sum(np.where(danger_map > 1, 1, 0))
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
