""" Solution to day 17

Lessons from the problem:
- use logic to reduce the range of loops
"""

import os
from functools import lru_cache
from typing import List, Tuple

from tqdm import tqdm

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


@lru_cache(maxsize=2**16)
def sum_of_integers(start: int, end: int) -> int:
    """ Returns the sum of integers from start to end """
    assert start <= end
    n_integers = (end - start) + 1
    return int((n_integers * (end + start)) / 2)
assert sum_of_integers(100, 100) == 100
assert sum_of_integers(0, 100) == 5050
assert sum_of_integers(10, 20) == 165
assert sum_of_integers(-100, 101) == 101


def find_acceptable_launches(x_target: List[int], y_target: List[int]) -> Tuple[int, int]:
    """ Finds the maximum achievable y for the target position """

    assert x_target[1] > x_target[0]
    assert y_target[1] > y_target[0]

    max_y = 0
    max_x_speed = x_target[1]
    distinct_valid_launches = 0

    # All directions pointing up will have a step with y=0 with speed=y_speed. This implies that
    # launches with y_speed > min y_target will always miss
    max_y_speed = -y_target[0]
    min_y_speed = y_target[0]
    max_steps = (max_y_speed * 2) + 1 # go up, go down to 0, move past the target

    # Gets min x speed to reach the x target given infinite steps, to speed up candidate search
    for mix_x_speed in range(max_steps):
        reachable_x = sum_of_integers(0, mix_x_speed)
        if reachable_x >= x_target[0]:
            break

    for y_speed in tqdm(range(min_y_speed, max_y_speed+1), "checking launches given y speed"):
        if y_speed > 0:
            this_max_y = sum_of_integers(0, y_speed)
            ascent_steps = y_speed
        else:
            this_max_y = 0
            ascent_steps = 0
        assert this_max_y >= 0
        assert ascent_steps >= 0

        admissible_descent = [this_max_y - y_target[1], this_max_y - y_target[0]]
        assert admissible_descent[0] < admissible_descent[1]

        descent_initial_speed = -min(0, y_speed)
        valid_steps = []
        assert descent_initial_speed >= 0
        for descent_steps in range(max_steps):
            descent = sum_of_integers(descent_initial_speed, descent_initial_speed+descent_steps)
            if descent < admissible_descent[0]:
                continue # not there yet
            elif descent > admissible_descent[1]:
                break # overshoot
            else:
                valid_steps.append(descent_steps + ascent_steps)

        if not valid_steps: # can't hit Y
            continue

        used_x_speeds = set()
        for steps in valid_steps:
            hits_x = False
            for x_speed in range(mix_x_speed, max_x_speed+1):
                x_pos = sum_of_integers(max((x_speed-steps), 0), x_speed)
                if x_pos < x_target[0]:
                    continue # not there yet
                elif x_pos > x_target[1]:
                    break # overshoot
                else:
                    # careful: the same x,y combination can be valid for multiple steps
                    if x_speed not in used_x_speeds:
                        distinct_valid_launches += 1
                    used_x_speeds.add(x_speed)
                    hits_x = True

            if not hits_x:
                continue
            if this_max_y > max_y:
                max_y = this_max_y

    return int(max_y), distinct_valid_launches


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    with open(os.path.join(DATA_PATH, "day_17.txt")) as input_file:
        for line in input_file:
            line = line.rstrip('\n')
            relevant_data = line[15:]
            x_0, x_1_y0, y_1 = relevant_data.split("..")
            x_1, y_0 = x_1_y0.split(", y=")
            x = [int(x_0), int(x_1)]
            y = [int(y_0), int(y_1)]

    max_y, distinct_valid_launches = find_acceptable_launches(x, y)
    problem_1 = max_y
    problem_2 = distinct_valid_launches
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
