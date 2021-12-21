""" Solution to day 15

Lessons from the problem:
-
"""

import os
from typing import Tuple

import numpy as np
import numpy.typing as npt
import networkx as nx

from aoc2021.utils import measure_time, print_results

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")

def pos_to_id(x: int, y: int, max_y: int) -> int:
    """ Convert a position in the grid to graph id"""
    return (x * max_y) + y


def find_min_traversal_risk(risk_matrix: npt.NDArray) -> int:
    """ Given the risk matrix, finds the minimum traversal risk from top left to bot right """
    G = nx.DiGraph()
    G.add_nodes_from(range(np.prod(risk_matrix.shape)))

    # adds the edges
    for x in range(risk_matrix.shape[0]):
        for y in range(risk_matrix.shape[1]):
            node_id = pos_to_id(x, y, risk_matrix.shape[1])
            next_pos = [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]
            valid_pos = []
            # filters out of range neighbours
            for pos in next_pos:
                if pos[0] < 0 or pos[0] >= risk_matrix.shape[0]:
                    continue
                if pos[1] < 0 or pos[1] >= risk_matrix.shape[1]:
                    continue
                valid_pos.append(pos)
            # adds directed edges to neighbours
            for pos in valid_pos:
                next_id = pos_to_id(pos[0], pos[1], risk_matrix.shape[1])
                G.add_edge(node_id, next_id, weight=risk_matrix[pos[0], pos[1]])

    path = nx.astar_path(G, 0, np.prod(risk_matrix.shape)-1)
    risk_sum = 0
    for idx in range(len(path)-1):
        src = path[idx]
        dst = path[idx+1]
        risk_sum += G[src][dst]["weight"]
    return risk_sum


def build_complete_risk_matrix(risk_matrix: npt.NDArray) -> npt.NDArray:
    """ Builds the complete risk matrix as instructed """
    x_len = risk_matrix.shape[0]
    y_len = risk_matrix.shape[1]
    complete_risk_matrix = np.zeros((x_len*5, y_len*5))
    for x in range(5):
        for y in range(5):
            x_start = x * x_len
            x_end = (x + 1) * x_len
            y_start = y * y_len
            y_end = (y + 1) * y_len
            complete_risk_matrix[x_start:x_end, y_start:y_end] = risk_matrix + x + y
    complete_risk_matrix[complete_risk_matrix > 9] -= 9
    return complete_risk_matrix.astype(int)


@measure_time
def get_solution() -> Tuple[int, int]:
    """ Solution to the problem """
    risk_list = []
    with open(os.path.join(DATA_PATH, "day_15.txt")) as input_file:
        for line in input_file:
            line = line.rstrip('\n')
            risk_list.append([int(risk) for risk in line])

    risk_matrix = np.asarray(risk_list, dtype=int)
    problem_1 = find_min_traversal_risk(risk_matrix)
    complete_risk_matrix = build_complete_risk_matrix(risk_matrix)
    problem_2 = find_min_traversal_risk(complete_risk_matrix)
    return problem_1, problem_2


if __name__ == "__main__":
    problem_1, problem_2, duration = get_solution()
    print_results(problem_1, problem_2, duration)
