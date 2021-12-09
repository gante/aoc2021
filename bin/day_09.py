""" Solution to day 09

Lessons from the problem:
-
"""

import os
from typing import List, Tuple

import numpy as np
import numpy.typing as npt

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def get_low_points(heights: npt.NDArray) -> npt.NDArray:
    """
    Returns the position of all low points
    """
    low_points = np.zeros(heights.shape, dtype=bool)
    for row in range(heights.shape[0]):
        for col in range(heights.shape[1]):
            height = heights[row, col]

            if row > 0:
                if height >= heights[row-1, col]:
                    continue
            if row < heights.shape[0] - 1:
                if height >= heights[row+1, col]:
                    continue

            if col > 0:
                if height >= heights[row, col-1]:
                    continue
            if col < heights.shape[1] - 1:
                if height >= heights[row, col+1]:
                    continue

            # has passed all checks, it is a low point
            low_points[row, col] = 1
    return low_points


def get_basin_sizes(heights: npt.NDArray, low_points: npt.NDArray) -> List[int]:
    """
    Given the heights and the low points, finds all basins. Returns their sizes. (Note: 9s are not
    part of any basins, and set the limits to them)
    """

    def get_valid_neighbours(x, y):
        neighbours = []
        if x > 0:
            neighbours.append((x-1, y))
        if x < heights.shape[0] - 1:
            neighbours.append((x+1, y))
        if y > 0:
            neighbours.append((x, y-1))
        if y < heights.shape[1] - 1:
            neighbours.append((x, y+1))
        valid_neighbours = [neighbour for neighbour in neighbours if heights[neighbour] < 9]
        return set(valid_neighbours)

    low_points_x, low_points_y = np.nonzero(low_points)
    basins_size = []
    for x, y in zip(low_points_x, low_points_y):
        checked_neighbours = set()
        unchecked_neighbours = get_valid_neighbours(x, y)
        while len(unchecked_neighbours):
            neighbour = unchecked_neighbours.pop()
            checked_neighbours.add(neighbour)
            unchecked_neighbours |= set(
                new_neighbour for new_neighbour in get_valid_neighbours(*neighbour)
                if new_neighbour not in checked_neighbours
            )
        basins_size.append(len(checked_neighbours))

    assert len(basins_size) == np.sum(low_points)
    return basins_size


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    with open(os.path.join(DATA_PATH, "day_09.txt")) as input_file:
        rows_of_heights = []
        for line in input_file:
            line = line.rstrip('\n')
            rows_of_heights.append([int(height) for height in line])

    heights = np.asarray(rows_of_heights)
    low_points = get_low_points(heights)
    problem_1 = int(np.sum(heights[low_points]) + np.sum(low_points))
    basin_sizes = get_basin_sizes(heights, low_points)
    basin_sizes.sort(reverse=True)
    problem_2 = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
