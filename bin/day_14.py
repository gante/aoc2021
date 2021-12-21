""" Solution to day 14

Lessons from the problem:
- When order is not needed, consider things as sets (or similar)
"""

import os
from typing import Dict, Tuple
from collections import defaultdict

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def insert_polymers(polymer: str, polymer_transformations: Dict[str, str], steps: int) -> str:
    """
    Insert polymers in the input polyme according to the transformation rules for the specified
    ammount of steps, returning the resulting polymer.
    """
    polymer_list = list(polymer)
    for _ in range(steps):
        new_polymer = []
        for idx in range(len(polymer_list) - 1):
            pair = polymer_list[idx] + polymer_list[idx+1]
            to_add = polymer_transformations[pair]
            new_polymer += [polymer_list[idx], to_add]
        new_polymer += [polymer_list[-1]]
        polymer_list = new_polymer
    return "".join(polymer_list)


def insert_polymers_wo_order(
    polymer: str,
    polymer_transformations: Dict[str, str],
    steps: int
) -> Dict[str, int]:
    """
    Same as the function above, but returns how many times a polymer is present in the chain. Part
    2 explodes with the function above.
    """
    # initialisation
    polymer_list = list(polymer)
    pair_counts: Dict[str, int] = defaultdict(int)
    for idx in range(len(polymer_list) - 1):
        pair = polymer_list[idx] + polymer_list[idx+1]
        pair_counts[pair] += 1

    # apply steps
    for _ in range(steps):
        new_pair_counts: Dict[str, int] = defaultdict(int)
        for pair in pair_counts:
            to_add = polymer_transformations[pair]
            new_pairs = [pair[0] + to_add, to_add + pair[1]]
            for new_pair in new_pairs:
                new_pair_counts[new_pair] += pair_counts[pair]
        pair_counts = new_pair_counts

    # count each polymer (pull the first letter of each pair)
    last_polymer = polymer_list[-1]
    polymer_counts: Dict[str, int] = defaultdict(int)
    for pair in pair_counts:
        polymer_counts[pair[0]] += pair_counts[pair]
    polymer_counts[last_polymer] += 1
    return polymer_counts


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    polymer_transformations = {}
    with open(os.path.join(DATA_PATH, "day_14.txt")) as input_file:
        for idx, line in enumerate(input_file):
            line = line.rstrip('\n')
            if idx == 0:
                input_polymer = line
            if idx > 1:
                line_transf = line.split(" -> ")
                polymer_transformations[line_transf[0]] = line_transf[1]

    output_polymer = insert_polymers(input_polymer, polymer_transformations.copy(), steps=10)
    polymer_counts = [output_polymer.count(char) for char in set(output_polymer)]
    problem_1 = max(polymer_counts) - min(polymer_counts)
    polymer_counts = list(insert_polymers_wo_order(
        input_polymer,
        polymer_transformations.copy(),
        steps=40
    ).values())
    problem_2 = max(polymer_counts) - min(polymer_counts)
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
