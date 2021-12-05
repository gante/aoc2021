""" Solution to day 04

Lessons from the problem:
-
"""

import os
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def find_desired_board(boards, number_sequence, win_idx):
    """
    Finds the desired board, given all the boards, the number sequence, and whether we want the
    index in which the board wins. Returns a tuple containing the winning board, its state
    (marked numbers), and the last number.
    """
    if win_idx < 0:
        win_idx = boards.shape[0] + win_idx

    board_state = np.zeros(boards.shape, dtype=bool)
    win_order = []
    win_order_set = set()
    for number in number_sequence:
        number_indexes = np.where(boards == number)
        board_state[number_indexes] = 1
        winning_rows = np.any(np.all(board_state, axis=1), axis=1)
        winning_cols = np.any(np.all(board_state, axis=2), axis=1)
        winning_boards = np.logical_or(winning_rows, winning_cols)
        for board_idx, board_has_won in enumerate(winning_boards):
            if board_has_won and board_idx not in win_order_set:
                win_order_set.add(board_idx)
                win_order.append(board_idx)

        if len(win_order)-1 >= win_idx:
            board_idx = win_order[win_idx]
            return boards[board_idx, ...], board_state[board_idx, ...], number


def get_solution():
    """ Solution to the problem """
    boards = []
    with open(os.path.join(DATA_PATH, "day_04.txt")) as input_file:
        for idx, line in enumerate(input_file):
            line = line.rstrip('\n')
            if idx == 0:
                number_sequence = [int(number) for number in line.split(",")]
            elif (idx - 1) % 6 == 0:
                boards.append([])
            else:
                boards[-1].append([int(number) for number in line.split(" ") if len(number)])

    boards = np.asarray(boards)
    board, board_state, last_number = find_desired_board(boards, number_sequence, win_idx=0)
    problem_1 = np.sum(board[~board_state]) * last_number
    board, board_state, last_number = find_desired_board(boards, number_sequence, win_idx=-1)
    problem_2 = np.sum(board[~board_state]) * last_number
    return problem_1, problem_2


if __name__ == "__main__":
    result_1, result_2 = get_solution()
    print(f"Solution to part 1: {result_1}")
    print(f"Solution to part 2: {result_2}")
