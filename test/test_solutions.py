""" Double-checks the outputs as the code evolves. That way, we can safely change
shared functions without breaking past solutions.

Possibly not the best testing structure, but gets the job done for now.
"""

import os
import time
from datetime import timedelta
import importlib
import pytest


SOLUTIONS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
    'bin',
)
SOLUTIONS = {
    1: (1466, 1491),
    2: (1882980, 1971232560),
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
    start = time.time()
    result = module.get_solution()
    end = time.time()
    assert result == SOLUTIONS[problem_idx], \
        "The result ({}) did not match the solution ({})!".format(result, SOLUTIONS[problem_idx])
    duration = timedelta(seconds=end-start)
    assert duration < timedelta(seconds=1), \
        "It took more than expected to run! (duration = {})".format(duration)