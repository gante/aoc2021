""" Double-checks the outputs as the code evolves. That way, we can safely change
shared functions without breaking past solutions.

Possibly not the best testing structure, but gets the job done for now.
"""

import os
from datetime import timedelta
import importlib
import pytest


MAX_TIME = 10 #seconds
SOLUTIONS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
    'bin',
)
SOLUTIONS = {
    1: (1466, 1491),
    2: (1882980, 1971232560),
    3: (1092896, 4672151),
    4: (25410, 2730),
    5: (8622, 22037),
    6: (351188, 1595779846729),
    7: (328318, 89791146),
    8: (369, 1031553),
    9: (512, 1600104),
    10: (243939, 2421222841),
    11: (1713, 502),
    12: (3679, 107395),
    13: (602, 0), # problem 2 here is a print in the terminal
    14: (4244, 4807056953866),
    15: (755, 3016),
    16: (984, 1015320896946),
    17: (6555, 4973),
}


def test_coverage():
    """ Tests whether all problems have a solution here. At most 1 problem may be missing its
    solution (the problem that is being worked on at the moment).
    """
    num_solutions = len(SOLUTIONS)
    num_problems = len(
        [f for f in os.listdir(SOLUTIONS_DIR) if os.path.isfile(os.path.join(SOLUTIONS_DIR, f))]
    )
    assert num_problems - num_solutions <= 1, \
        "Missing solutions! ({} problems, {} solutions)".format(num_problems, num_solutions)


@pytest.mark.parametrize("problem_idx", list(SOLUTIONS.keys()))
def test_results(problem_idx):
    """ Tests whether the solutions of the problems are correct and that they run within a minute.
    """
    if problem_idx < 10:
        module_termination = "0" + str(problem_idx)
    else:
        module_termination = str(problem_idx)
    module_name = "bin.day_" + module_termination
    module = importlib.import_module(module_name)
    result_0, result_1, duration = module.get_solution()
    result = (result_0, result_1)
    assert result == SOLUTIONS[problem_idx], \
        "The result ({}) did not match the solution ({})!".format(result, SOLUTIONS[problem_idx])
    assert duration < timedelta(seconds=MAX_TIME), \
        "It took more than expected to run! (duration = {})".format(duration)
