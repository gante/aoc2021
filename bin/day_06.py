""" Solution to day 06

Lessons from the problem:
-
"""

import os
from typing import Dict, List, Tuple

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def parse_fish_timer(input_data: List[str]) -> Dict[int, int]:
    """
    Converts the input into a dict, where the key is the number of days until the fish reproduces,
    and the value is the number of fishes in that state
    """
    fish_timer = {key: 0 for key in range(9)}
    for days_until_multiplication in input_data:
        fish_timer[int(days_until_multiplication)] += 1
    return fish_timer


def advance_days(input_fish_timer: Dict[int, int], days: int) -> Dict[int, int]:
    """
    Applies the problem logic for the number of specified days (new fish when timer goes below 0,
    where the new fish requires 8 days to reproduce and the old fish just 6)
    """
    fish_timer = input_fish_timer.copy() # no side-effects
    for _ in range(days):
        start_fish_timer = fish_timer
        fish_timer = {key: 0 for key in range(9)}
        for days_left in start_fish_timer:
            if days_left == 0:
                fish_timer[8] += start_fish_timer[days_left]
                fish_timer[6] += start_fish_timer[days_left]
            else:
                fish_timer[days_left-1] += start_fish_timer[days_left]
    return fish_timer


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    with open(os.path.join(DATA_PATH, "day_06.txt")) as input_file:
        for line in input_file:
            line = line.rstrip('\n')
            input_data = line.split(",")

    input_fish_timer = parse_fish_timer(input_data)
    fish_timer = advance_days(input_fish_timer, days=80)
    problem_1 = sum([n_fishes for n_fishes in fish_timer.values()])
    fish_timer = advance_days(input_fish_timer, days=256)
    problem_2 = sum([n_fishes for n_fishes in fish_timer.values()])
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
