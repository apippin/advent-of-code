from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
import pandas as pd
import numpy as np

# What day and year is this solution for?
day = 9
year = 2023

# Game globals
...

# Sample game data:
# 0 3 6 9 12 15
# 1 3 6 10 15 21
# 10 13 16 21 30 45
raw = aoc_helper.fetch(day, year)

# ...
def parse_raw(raw: str):
    lines = raw.splitlines()
    data = list()
    for line in lines:
        data.append(list(map(int, re.findall(r"(\d+)", line))))
    return data

# Parse the game data
data = parse_raw(raw)

# Analyze your OASIS report and extrapolate the next value for each history.
# What is the sum of these extrapolated values?
def part_one(data=data):
    #print(f"{data}")
    for hist in data:
        diffs = []
        diffs.append(pd.Series(hist))
        while diffs[-1].any():
            diffs.append(diffs[-1].diff())
        print(f"{diffs}")
        for diff in diffs:
            val = int(np.nan_to_num(diff.iat[-1]))
            print(f"{val} ")
        next_val = sum(int(np.nan_to_num(val.iat[-1])) for val in diffs)
        hist.append(next_val)
    print(*data,sep='\n')
    next_val_sum = sum(vals[-1] for vals in data)
    print(f"next_val_sum: {next_val_sum}")
    return next_val_sum
# ...
def part_two(data=data):
    ...

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
#aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
#aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
