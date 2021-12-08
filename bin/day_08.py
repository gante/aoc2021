""" Solution to day 08

Lessons from the problem:
- frozenset saves lifes in unordered pattern matching
"""

import os
from typing import Dict, List, Tuple

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


SEVEN_SEG_MAP = {
    frozenset("abcefg"): 0,
    frozenset("cf"): 1,
    frozenset("acdeg"): 2,
    frozenset("acdfg"): 3,
    frozenset("bcdf"): 4,
    frozenset("abdfg"): 5,
    frozenset("abdefg"): 6,
    frozenset("acf"): 7,
    frozenset("abcdefg"): 8,
    frozenset("abcdfg"): 9
}


def count_1_4_7_8(data_list: List[str]) -> int:
    """ Counts the substrings with specific lengths corresponding to the digits above """
    count = 0
    for data in data_list:
        substrings = data.split(" ")
        for substring in substrings:
            if len(substring) in (2, 3, 4, 7):
                count += 1
    return count


def get_decoding(context: str) -> Dict[str, str]:
    """ Returns a dictionary with the segment correspondence, given the context (e.g. a -> g) """
    all_chars = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
    char_count = {char: 0 for char in all_chars}
    substrings = context.split(" ")
    for substring in substrings:
        if len(substring) == 2:
            digit_1 = set(substring)
        if len(substring) == 3:
            digit_7 = set(substring)
        if len(substring) == 4:
            digit_4 = set(substring)
        for char in substring:
            char_count[char] += 1
    rev_char_count: Dict[int, set] = {rev_count: set() for rev_count in range(7)}
    for char, count in char_count.items():
        rev_char_count[10 - count].add(char)
    assert len(rev_char_count[4]) == len(rev_char_count[6]) == len(rev_char_count[1]) == 1

    encodings = {}
    encodings["a"] = list(digit_7 - digit_1)[0]
    encodings["b"] = list(rev_char_count[4])[0]
    encodings["e"] = list(rev_char_count[6])[0]
    encodings["f"] = list(rev_char_count[1])[0]

    encodings["c"] = list(rev_char_count[2] - set(encodings["a"]))[0]
    encodings["d"] = list(digit_4 - {v for k, v in encodings.items() if k in ("b", "c", "f")})[0]
    encodings["g"] = list(rev_char_count[3] - set(encodings["d"]))[0]

    decoding_map = {v: k for k, v in encodings.items()}
    assert len(decoding_map) == 7
    assert len(set(decoding_map.keys())) == 7
    assert len(set(decoding_map.values())) == 7
    return decoding_map


def apply_decoding(substrings: List[str], decoding_map: Dict[str, str]) -> List[str]:
    """ Applies decoding on the data """
    decoded_substrings = []
    for substring in substrings:
        decoded_substrings.append("".join([decoding_map[char] for char in substring]))
    return decoded_substrings


def sum_decoded_data(data_list: List[str], context_list: List[str]) -> int:
    """ Decodes using the context and accumulates the numbers in the data """
    all_ints = []
    for data, context in zip(data_list, context_list):
        decoding_map = get_decoding(context)
        substrings = data.split(" ")
        decoded_substrings = apply_decoding(substrings, decoding_map)
        int_sequence = []
        for substring in decoded_substrings:
            int_sequence.append(SEVEN_SEG_MAP[frozenset(substring)])
        all_ints.append(sum(digit*(10**idx) for idx, digit in enumerate(int_sequence[::-1])))
    return sum(all_ints)


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    context_list = []
    data_list = []
    with open(os.path.join(DATA_PATH, "day_08.txt")) as input_file:
        for line in input_file:
            line = line.rstrip('\n')
            input_data = line.split(" | ")
            context_list.append(input_data[0])
            data_list.append(input_data[1])

    problem_1 = count_1_4_7_8(data_list)
    problem_2 = sum_decoded_data(data_list, context_list)
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
