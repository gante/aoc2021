""" Solution to day 13

Lessons from the problem:
-
"""

import os
from typing import Any, List, Tuple

import numpy as np
import numpy.typing as npt

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def fold(dot_matrix: npt.NDArray, fold_instructions: List[List[str]], n_folds: int) -> npt.NDArray:
    """ Counts how many dots are there after the first fold"""
    for idx in range(n_folds):
        if fold_instructions[idx][0] == "x":
            x_fold = int(fold_instructions[idx][1])
            padding_length = (x_fold * 2) - dot_matrix.shape[0] + 1
            if padding_length != 0:
                if padding_length > 0:
                    dot_matrix = np.pad(dot_matrix, ((0, padding_length), (0, 0)), 'constant')
                else:
                    dot_matrix = np.pad(dot_matrix, ((-padding_length, 0), (0, 0)), 'constant')
            dot_matrix = dot_matrix[:x_fold, :] + dot_matrix[x_fold+1:, :][::-1, :]
        else:
            y_fold = int(fold_instructions[idx][1])
            padding_length = (y_fold * 2) - dot_matrix.shape[1] + 1
            if padding_length != 0:
                if padding_length > 0:
                    dot_matrix = np.pad(dot_matrix, ((0, 0), (0, padding_length)), 'constant')
                else:
                    dot_matrix = np.pad(dot_matrix, ((0, 0), (-padding_length, 0)), 'constant')
            dot_matrix = dot_matrix[:, :y_fold] + dot_matrix[:, y_fold+1:][:, ::-1]
    return dot_matrix.astype(bool)


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    coordinate_pairs = []
    fold_instructions = []
    with open(os.path.join(DATA_PATH, "day_13.txt")) as input_file:
        parsing_fold = False
        for line in input_file:
            line = line.rstrip('\n')
            if not line:
                parsing_fold = True
                continue
            if parsing_fold:
                fold_line = line.split(" ")
                fold_instructions.append([fold_line[2][0], fold_line[2][2:]])
            else:
                coordinate_pairs.append([int(pos) for pos in line.split(",")])

    x_max = max([pos[0] for pos in coordinate_pairs]) + 1
    y_max = max([pos[1] for pos in coordinate_pairs]) + 1
    dot_matrix = np.zeros((x_max, y_max), dtype=int)
    for (x, y) in coordinate_pairs:
        dot_matrix[x, y] = 1
    assert np.sum(dot_matrix) == len(coordinate_pairs)

    problem_1 = np.sum(fold(np.copy(dot_matrix), fold_instructions, n_folds=1))
    problem_2 = 0 # depends on print below
    problem_2_out = fold(np.copy(dot_matrix), fold_instructions, n_folds=12)

    # should print CAFJHZCK
    for y in range(problem_2_out.shape[1]):
        for x in range(problem_2_out.shape[0]):
            if problem_2_out[x, y]:
                print("# ", end="", flush=True)
            else:
                print("  ", end="", flush=True)
        print("\n", end="", flush=True)
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
