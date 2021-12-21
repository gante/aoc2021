""" Solution to day 16

Lessons from the problem:
- `int` accepts a 2nd argument, which is the base :o
"""

import os
from typing import Tuple

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def hex_to_bin(hex: str) -> str:
    """ Self documenting ;) """
    return bin(int(hex, 16))[2:].zfill(len(hex)*4)


def version_bin_to_int(version: str) -> int:
    """ Converts an integer of 3 bits to int"""
    assert len(version) == 3
    return int(version, 2)


def type_bin_to_int(packet_type: str) -> int:
    """ Converts an integer of 3 bits to int"""
    assert len(packet_type) == 3
    return int(packet_type, 2)


def parse_literal(binary:str) -> Tuple[int, int]:
    """ Parses the binary contents of a literal, returning the value and the binary length"""
    binary_value = ""
    literal_length = 0
    while binary[0] == "1":
        literal_length += 5
        binary_value += binary[1:5]
        binary = binary[5:]
    # last values from the literal
    literal_length += 5
    binary_value += binary[1:5]
    return int(binary_value, 2), literal_length


def sum_versions(binary: str) -> Tuple[int, str]:
    """
    Parses the binary, returning the sum of the versions of the contained packages and the
    remaining binary string. Intended to use recursively.
    """
    accumulated_versions = 0
    version = binary[:3]
    accumulated_versions += version_bin_to_int(version)
    packet_type = binary[3:6]
    remaining_binary = binary[6:]
    if packet_type == "100": # literal
        _, literal_length = parse_literal(remaining_binary)
        return accumulated_versions, remaining_binary[literal_length:]
    else: # operator
        if remaining_binary[0] == "0": # 15 next bits with length of the packet
            length = int(remaining_binary[1:16], 2)
            remaining_binary = remaining_binary[16:]
            while length > 0:
                subpacket_versions, subpacket_binary = sum_versions(remaining_binary)
                accumulated_versions += subpacket_versions
                length -= len(remaining_binary) - len(subpacket_binary)
                remaining_binary = subpacket_binary
            assert length == 0
        else: # 11 next bits depicting number of subpackets
            n_subpacets = int(remaining_binary[1:12], 2)
            remaining_binary = remaining_binary[12:]
            for _ in range(n_subpacets):
                subpacket_versions, subpacket_binary = sum_versions(remaining_binary)
                accumulated_versions += subpacket_versions
                remaining_binary = subpacket_binary
    return accumulated_versions, remaining_binary


def decode_binary(binary: str) -> Tuple[int, str]:
    """ Decodes the binary. Intended to use recursivelly"""
    value = 0
    packet_type = type_bin_to_int(binary[3:6])
    remaining_binary = binary[6:]
    if packet_type == 4: # literal
        literal_value, literal_length = parse_literal(remaining_binary)
        value = literal_value
        remaining_binary = remaining_binary[literal_length:]
    else: # operator
        if remaining_binary[0] == "0": # 15 next bits with length of the packet
            length = int(remaining_binary[1:16], 2)
            remaining_binary = remaining_binary[16:]
            values = []
            while length > 0:
                subpacket_value, subpacket_binary = decode_binary(remaining_binary)
                values.append(subpacket_value)
                length -= len(remaining_binary) - len(subpacket_binary)
                remaining_binary = subpacket_binary
            assert length == 0
        else: # 11 next bits depicting number of subpackets
            n_subpacets = int(remaining_binary[1:12], 2)
            remaining_binary = remaining_binary[12:]
            values = []
            for _ in range(n_subpacets):
                subpacket_value, subpacket_binary = decode_binary(remaining_binary)
                values.append(subpacket_value)
                remaining_binary = subpacket_binary
        # applies the operation
        if packet_type == 0:
            value = sum(values)
        elif packet_type == 1:
            value = 1
            for val in values:
                value *= val
        elif packet_type == 2:
            value = min(values)
        elif packet_type == 3:
            value = max(values)
        elif packet_type == 5:
            assert len(values) == 2
            value = 1 if values[0] > values[1] else 0
        elif packet_type == 6:
            assert len(values) == 2
            value = 1 if values[0] < values[1] else 0
        elif packet_type == 7:
            assert len(values) == 2
            value = 1 if values[0] == values[1] else 0
        else:
            raise ValueError(f"{packet_type} is not a valid packet type")

    return value, remaining_binary


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    with open(os.path.join(DATA_PATH, "day_16.txt")) as input_file:
        for line in input_file:
            hex = line.rstrip('\n')

    binary = hex_to_bin(hex)
    assert len(binary) == len(hex)*4
    problem_1, _ = sum_versions(binary)
    problem_2, _ = decode_binary(binary)
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
