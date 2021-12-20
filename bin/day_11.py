""" Solution to day 11

Lessons from the problem:
- `energy_levels > 9` returns a 2D boolean array, not the positions where the condition is true :v
- be mindful of in-place numpy array updates -- my initial solution did not copy the input array,
    causing the solution to problem 2 to be wrong by 100 steps
"""

import os
from typing import Tuple

import numpy as np
import numpy.typing as npt
from scipy import signal
from tqdm import tqdm

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def simulate_flashes(
    input_energy_levels: npt.NDArray,
    steps: int,
    window_size: int
) -> Tuple[int, int]:
    """
    Simulates the evolution of the flashes for N steps, given the initial energy levels. The window
    size depicts how far a flash excites other octupi. Breaks when all octupi are synchronized

    Returns the total number of flashes and the number of simulation steps.
    """
    energy_levels = np.copy(input_energy_levels)
    total_flashes = 0
    synch_step = 0
    window_conv = np.ones((window_size, window_size), dtype=int)
    for step in tqdm(range(1, steps+1), "Simulating steps"):
        has_flashed = np.zeros(energy_levels.shape, dtype=bool)
        energy_levels += 1
        while np.sum(energy_levels > 9):
            flash_positions = energy_levels > 9
            has_flashed[flash_positions] = True
            # Sets to a negative number to avoid reflashing
            energy_levels[flash_positions] = - np.prod(energy_levels.shape) - 100000000
            # Adds energy around the flash positions
            energy_levels += signal.convolve2d(
                np.asarray(flash_positions, dtype=int),
                window_conv,
                mode="same"
            )
        # Resets the energy of the flashes
        energy_levels[energy_levels < 0] = 0
        total_flashes += np.sum(has_flashed, dtype=int)
        # If all of them flash, stop
        if np.sum(has_flashed, dtype=int) == np.prod(energy_levels.shape):
            synch_step = step
            break

    return total_flashes, synch_step


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    with open(os.path.join(DATA_PATH, "day_11.txt")) as input_file:
        energy_input = []
        for line in input_file:
            line = line.rstrip('\n')
            energy_input.append([int(energy) for energy in line])

    energy_levels = np.asarray(energy_input)

    problem_1, _ = simulate_flashes(energy_levels, steps=100, window_size=3)
    _, problem_2 = simulate_flashes(energy_levels, steps=1000, window_size=3)
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
