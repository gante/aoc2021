""" Solution to day 12

Lessons from the problem:
- Careful with mutating variables (again :scream:)
- Lists faster than tuples when continuously appending (doh), but be mindful of the lesson above
"""

import os
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def get_paths(
    cave_connections: Dict[str, List[str]],
    current_cave: str,
    visited_caves: Optional[Set[str]] = None,
    existing_paths: Optional[List[List[str]]] = None,
    cave_visited_twice: Optional[str] = None,
) -> List[List[str]]:
    """ Gets all possible paths from the current cave, given the visited caves"""

    def _add_cave_to_paths(cave: str, all_paths: List[List[str]]) -> List[List[str]]:
        new_paths = []
        for path in all_paths:
            new_paths.append(path + [cave,])
        return new_paths

    if existing_paths is None:
        existing_paths = [["start",]]
    else:
        existing_paths = _add_cave_to_paths(current_cave, existing_paths)

    # exit condition 1: we are at the end
    if current_cave == "end":
        return existing_paths

    if visited_caves is None:
        visited_caves = set()
    if current_cave in visited_caves:
        cave_visited_twice = current_cave
    if not current_cave.isupper():
        visited_caves.add(current_cave)

    # exit consition 2: no more caves to explore
    possible_next_caves = set(cave_connections[current_cave]) - visited_caves
    if cave_visited_twice is None:
        possible_next_caves |= set(cave_connections[current_cave]) - set(["start"])
    if not possible_next_caves:
        return [["dummy", ]] # Nothing of value out of this return

    paths = []
    for next_cave in possible_next_caves:
        assert next_cave != "start", "Can't go back to the start"
        downsteam_paths = get_paths(
            cave_connections,
            next_cave,
            visited_caves.copy(),
            existing_paths.copy(),
            cave_visited_twice
        )
        paths.extend([path for path in downsteam_paths if path[-1] == "end"])
    return paths


def count_paths(cave_connections: Dict[str, List[str]]) -> int:
    """
    Returns the number of paths between start and end, given cave connections (format:
    {start: [end_0, end_1]}). Capitalised caves can be used more than once in a path.
    """
    paths = get_paths(cave_connections, "start", cave_visited_twice="dummy")
    return len(paths)


def count_paths_visit_one_small_twice(cave_connections: Dict[str, List[str]]) -> int:
    """
    Same as above, but can visit a small cave twice
    """
    paths = get_paths(cave_connections, "start")
    return len(paths)


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    cave_connections = defaultdict(list)
    with open(os.path.join(DATA_PATH, "day_12.txt")) as input_file:
        for line in input_file:
            line = line.rstrip('\n')
            start, end = line.split("-")
            cave_connections[start].append(end)
            # also adds the reverse path
            cave_connections[end].append(start)

    problem_1 = count_paths(cave_connections)
    problem_2 = count_paths_visit_one_small_twice(cave_connections)
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
