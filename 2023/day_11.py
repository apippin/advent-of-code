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

# 1) Read in universe where galaxies are marked with #
# 2) Expand the universe by doubling the empty rows and cols (without galaxies in them)
def parse_raw(raw: str):
    global galaxies
    lines = raw.splitlines()
    data = []
    for line in lines:
        data.append(list(line))
        # If the row does not contain any galaxies, expand the galaxy
        if '#' not in line:
            data.append(list(line))

    # If the col does not contain any galaxies, expand the galaxy by adding another column
    orig_matrix = np.array(data)
    matrix = orig_matrix
    added_cols = 0
    for col in range(0, len(data[0])):
        # If a column contains no galaxies, insert a new column there
        if np.all(orig_matrix[:, col] == '.'):
            matrix = np.insert(matrix, col + added_cols, '.', axis=1)
            added_cols += 1
    data = matrix.tolist()

    return data

# Parse the game data
data = parse_raw(raw)

# Calculate the distance between 2 galaxies cartesian coordinates
def calc_distance(g1, g2):
    return abs(g2[1]-g1[1]) + abs(g2[0]-g1[0])

# Expand the universe, then find the length of the shortest path between every pair of galaxies.
# What is the sum of these lengths?
def part_one(data=data):
    #print(*data,sep='\n')

    # Number all the galaxies in increasing numbers, store their locations in cartesian coordinates
    galaxies = []
    for grow, line in enumerate(data):
        try:
            for gcol in indexes(line, '#'):
                galaxies.append((grow, gcol))
        except:
            continue
    #print(*galaxies,sep='\n')

    # Calculate the distance between each galaxy pairs
    sum_of_paths = 0
    for a, g1 in enumerate(galaxies):
        for b,g2 in enumerate(galaxies):
            if b > a:
                sum_of_paths += calc_distance(g1, g2)
    print(f"sum_of_paths: {sum_of_paths}")
    return sum_of_paths

# Starting with the same initial image, expand the universe according to these new rules,
# then find the length of the shortest path between every pair of galaxies.
# What is the sum of these lengths?
def part_two(data=data):
    ...

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
#aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
