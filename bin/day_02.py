""" Solution to day 02

Lessons from the problem:
-
"""

import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def get_final_position(direction_list, values_list):
    """
    Given the list of movements, returns a tuple with the final horizontal position and depth
    """
    horizontal = 0
    aim = 0
    depth = 0
    for direction, value in zip(direction_list, values_list):
        if direction == "up":
            aim = aim - value
        elif direction == "down":
            aim = aim + value
        elif direction == "forward":
            horizontal = horizontal + value
            depth = depth + (aim * value)
        else:
            raise ValueError("Unexpected direction")
    return horizontal, depth, aim


def get_solution():
    """ Solution to the problem """
    values_list = []
    direction_list = []
    with open(os.path.join(DATA_PATH, "day_02.txt")) as input_file:
        for line in input_file:
            line.strip()
            line_parts = line.split(" ")
            direction_list.append(line_parts[0])
            values_list.append(int(line_parts[1]))

    horizontal, depth, aim, = get_final_position(direction_list, values_list)
    problem_1 = horizontal * aim # problem 1 uses aim as depth
    problem_2 = horizontal * depth
    return problem_1, problem_2


if __name__ == "__main__":
    result_1, result_2 = get_solution()
    print(f"Solution to part 1: {result_1}")
    print(f"Solution to part 2: {result_2}")
