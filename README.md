# Advent of Code 2021

Solutions of the problems in AoC2021, using `Python`. Trying to focus on:
* high-performance solutions
* pure functions


## Running Requirements


Please create a new virtual environment with Python 3.7. For specific package requirements, check setup.cfg (running pip install -e . from the repo root folder should install all needed requirements).

## Structure

The input data is available in the `data/` folder, as `data_DD.txt`, where `DD` is the day of the problem. The scripts to compute the answer to the challenges are available in the `bin/` folder.

The solution for each day contains a `get_solution()` function, which returns the two answers. The answers are tested for correcness and time (see `test/`), which enables tinkering with the code without losing the desired properties.
