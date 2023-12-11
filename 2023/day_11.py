from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
import numpy as np

# What day and year is this solution for?
day = 11
year = 2023

# Sample game data:
"""
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
raw = aoc_helper.fetch(day, year)

# Return a list of indexes in string or list that matches ch
def indexes(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

# Globals
expansion_factor = 1
#expansion_factor = 100
#expansion_factor = 1000000

# 1) Read in universe where galaxies are marked with #
# 2) Expand the universe by doubling the empty rows and cols (without galaxies in them)
def parse_raw(raw: str):
    lines = raw.splitlines()
    data = dict()
    data["matrix"] = []
    data["galaxies"] = []
    data["expanded_rows"] = []
    data["expanded_cols"] = []
    for row,line in enumerate(lines):
        data["matrix"].append(list(line))
        # If the row does not contain any galaxies, expand the galaxy
        if '#' not in line:
            data["expanded_rows"].append(row)

    # If the col does not contain any galaxies, expand the galaxy by adding another column
    orig_matrix = np.array(data["matrix"])
    matrix = orig_matrix
    added_cols = 0
    for col in range(0, len(data["matrix"][0])):
        # If a column contains no galaxies, insert a new column there
        if np.all(orig_matrix[:, col] == '.'):
            data["expanded_cols"].append(col)

    # Number all the galaxies in increasing numbers, store their locations in cartesian coordinates
    for grow, line in enumerate(data["matrix"]):
        try:
            for gcol in indexes(line, '#'):
                data["galaxies"].append((grow, gcol))
        except:
            continue

    return data

# Parse the game data
data = parse_raw(raw)

# Calculate the distance between 2 galaxies cartesian coordinates
def calc_distance(data, g1, g2, expansion_factor):
    # account for the expansion factor in the rows
    erows = data["expanded_rows"]
    expanded_rows_crossed = len(set(erows).intersection(set(range(min(g1[0], g2[0]), max(g1[0], g2[0])))))
    rows = (abs(g2[0]-g1[0])) + (expanded_rows_crossed*expansion_factor)

    # account for the expansion factor in the cols
    ecols = data["expanded_cols"]
    expanded_cols_crossed = len(set(ecols).intersection(set(range(min(g1[1], g2[1]), max(g1[1], g2[1])))))
    cols = (abs(g2[1]-g1[1])) + (expanded_cols_crossed*expansion_factor)

    # calculate distance
    distance = rows + cols
    return distance

# Expand the universe, then find the length of the shortest path between every pair of galaxies.
# What is the sum of these lengths?
def part_one(data=data, expansion_factor=2):
    print(*data["matrix"],sep='\n')
    print(f"galaxies: {data['galaxies']}")
    print(f"erows: {data['expanded_rows']}")
    print(f"ecols: {data['expanded_cols']}")

    # Calculate the distance between each galaxy pairs
    sum_of_paths = 0
    for a, g1 in enumerate(data["galaxies"]):
        for b,g2 in enumerate(data["galaxies"]):
            if b > a:
                distance = calc_distance(data, g1, g2, expansion_factor-1)
                #print(f"{g1} -> {g2} distance: {distance}")
                sum_of_paths += distance
    print(f"sum_of_paths: {sum_of_paths}")
    return sum_of_paths

# Starting with the same initial image, expand the universe according to these new rules,
# then find the length of the shortest path between every pair of galaxies.
# What is the sum of these lengths?
def part_two(data=data):
    return part_one(data, 1000000)


# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
