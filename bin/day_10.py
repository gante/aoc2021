""" Solution to day 10

Lessons from the problem:
- Asserts help you confirm assumptions and avoid silly mistakes :)
"""

import os
from typing import List, Tuple

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")

CHARS_MATCHES = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}
OPENING_CHARS = set(CHARS_MATCHES.keys())
CLOSING_CHARS = set(CHARS_MATCHES.values())
ILLEGAL_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
AUTOCOMPLETE_POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def count_illegal_points(lines_of_chunks: List[str]) -> Tuple[int, List[str]]:
    """ Counts the number of points in the illegal lines """
    uncorrupt_lines = []
    points = 0
    for line in lines_of_chunks:
        open_chunk = []
        is_corrupt = False
        for char in line:
            if char in OPENING_CHARS:
                open_chunk.append(char)
            if char in CLOSING_CHARS:
                matching_char = open_chunk.pop()
                if CHARS_MATCHES[matching_char] != char:
                    points += ILLEGAL_POINTS[char]
                    is_corrupt = True
                    break
        if not is_corrupt:
            uncorrupt_lines.append(line)
    assert len(uncorrupt_lines) % 2 == 1 # the problem says it's always an odd number
    return points, uncorrupt_lines


def count_autocomplete_points(uncorrupt_lines: List[str]) -> List[int]:
    """ Counts the number of points when autocompleting incomplete lines """
    points = []
    for line in uncorrupt_lines:
        open_chunk = []
        for char in line:
            if char in OPENING_CHARS:
                open_chunk.append(char)
            if char in CLOSING_CHARS:
                open_chunk.pop()
        # time to autocomplete -- go through the open chunk in reverse order
        closing_chunk = [CHARS_MATCHES[char] for char in open_chunk[::-1]]
        line_points = 0
        for char in closing_chunk:
            line_points *= 5
            line_points += AUTOCOMPLETE_POINTS[char]
        points.append(line_points)
    return points


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    lines_of_chunks = []
    with open(os.path.join(DATA_PATH, "day_10.txt")) as input_file:
        for line in input_file:
            line = line.rstrip('\n')
            lines_of_chunks.append(line)

    corrupt_points, uncorrupt_lines = count_illegal_points(lines_of_chunks)
    problem_1 = corrupt_points
    autocomplete_points = sorted(count_autocomplete_points(uncorrupt_lines))
    problem_2 = autocomplete_points[len(autocomplete_points)//2]
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
