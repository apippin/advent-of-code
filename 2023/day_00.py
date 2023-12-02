from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
import operator
from functools import reduce

# What day and year is this solution for?
day = 1
year = 2023

# Game globals
...

# Sample game data:
# ...
raw = aoc_helper.fetch(day, year)

# ...
def parse_raw(raw: str):
    lines = raw.splitlines()
    data = lines
    return data

# Parse the game data
data = parse_raw(raw)

# ...
def part_one(data=data):
    ...

# ...
def part_two(data=data):
    ...

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
