from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
import functools

# What day and year is this solution for?
day = 12
year = 2023

# Sample game data:
"""
#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1
"""
"""
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
raw = aoc_helper.fetch(day, year)

# ...
def parse_raw(raw: str):
    lines = raw.splitlines()
    data = {}
    data["records"] = []
    for line in lines:
        records, groups = line.split()
        groups = [int(x) for x in groups.split(",")]
        data["records"].append([records, groups])
    return data

# Parse the game data
data = parse_raw(raw)

# For a given data record and groups, determine if it satisfies the group
# r = position within the record
# g = position within the groups
# l = length of current group in the record where we are at
# keep track if the tuple (r, g, l) is an arrangement or not
arrangement_dict = {}
def find_arrangements(record, r, g, l):
    key = (r, g, l)
    # If we already have an answer for this arrangement, return it now
    if key in arrangement_dict:
        return arrangement_dict[key]
    # If we have reached the end of our record string, check if we found an arrangement
    if r == len(record[0]):
        if g == len(record[1]) and l == 0:
            return 1
        elif g == len(record[1])-1 and record[1][g] == l:
            return 1
        else:
            return 0
    arrangement = 0
    for c in ['.', '#']:
        if record[0][r] == c or record[0][r] == '?':
            if c == '.' and l == 0:
                arrangement += find_arrangements(record, r+1, g, 0)
            elif c == '.' and l > 0 and g < len(record[1]) and record[1][g] == l:
                arrangement += find_arrangements(record, r+1, g+1, 0)
            elif c == '#':
                arrangement += find_arrangements(record, r+1, g, l+1)
    arrangement_dict[key] = arrangement
    return arrangement

# For each row, count all of the different arrangements of operational and
# broken springs that meet the given criteria. What is the sum of those counts?
def part_one(data=data):
    #print(f"{data}")
    global arrangement_dict
    sum_of_arrangements = 0
    for record in data["records"]:
        #print(f"{record}")
        arrangement_dict = {}
        arrangements = find_arrangements(record, 0, 0, 0)
        #print(f"arrangements: {arrangements}")
        sum_of_arrangements += arrangements
    print(f"sum_of_arrangements: {sum_of_arrangements}")
    return sum_of_arrangements

# Unfold your condition records; what is the new sum of possible arrangement counts?
def part_two(data=data):
    global arrangement_dict
    sum_of_arrangements = 0
    for record in data["records"]:
        #print(f"{record}")
        arrangement_dict = {}
        # unfold the record
        record[0] = '?'.join([record[0], record[0], record[0], record[0], record[0]])
        record[1] = record[1] + record[1] + record[1] + record[1] + record[1]
        #print(f"{record}")
        arrangements = find_arrangements(record, 0, 0, 0)
        #print(f"arrangements: {arrangements}")
        sum_of_arrangements += arrangements
    print(f"sum_of_arrangements: {sum_of_arrangements}")
    return sum_of_arrangements

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
