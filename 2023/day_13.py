from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re

# What day and year is this solution for?
day = 13
year = 2023

# Game globals
debug = 0

# Sample game data:
"""
123456789
    ><
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><
123456789
"""
"""
1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7
"""
raw = aoc_helper.fetch(day, year)

# Store the rows and cols as list of strings so they are easy to compare
def parse_raw(raw: str):
    lines = raw.splitlines()
    data = []
    p = 0
    for line in lines:
        if not line:
            p += 1
            continue
        if p >= len(data):
            data.append({})
            data[p]["rows"] = []
            data[p]["cols"] = []
        # Store each row as a list of strings
        data[p]["rows"].append(line)
        # Store each column as a list of strings
        for i,c in enumerate(line):
            if i >= len(data[p]["cols"]):
                data[p]["cols"].append(c)
            else:
                data[p]["cols"][i] += c
    return data

# Parse the game data
data = parse_raw(raw)

# Find all the consecutive item pairs that match each other and return the list of them
def find_adjacent_match(items):
    matches = []
    for i, a in enumerate(items):
        if (i+1 < len(items)) and (items[i] == items[i+1]):
            matches.append((i, i+1))
    #matches.append((-1, -1))
    return matches

# Find the line of reflection in each of the patterns in your notes.
# What number do you get after summarizing all of your notes?
def part_one(data=data):
    #print(f"{data}")
    sum_of_summaries = 0
    for p,pattern in enumerate(data,1):
        rows = pattern["rows"]
        cols = pattern["cols"]
        if debug:
            print(f"{p}: rows:")
            print(*rows,sep='\n')
            print(f"{p}: cols:")
            print(*cols,sep='\n')
        for items in (rows, cols):
            if items == rows:
                items_name = "rows"
            else:
                items_name = "cols"
            # Find all of the adjacent matches in this list of items
            adjacent_matches = find_adjacent_match(items)
            # Go through each adjacent_matches while we haen't found a reflection and we still have adjacent matches to check
            summary = 0
            for match in adjacent_matches:
                if debug:
                    print(f"{p}: {items_name} match: {match}")
                if match[0] >= 0:
                    a = match[0]
                    b = match[1]
                    while (a >= 0 and b < len(items)) and (items[a] == items[b]):
                        a -= 1
                        b += 1
                    # If either edge hit a boundary and we still matched, we found a valid reflection
                    if debug:
                        print(f"{p}: a:{a} b:{b} items:{len(items)}")
                    if a < 0 or b >= len(items):
                        if items == rows:
                            summary = 100 * (match[1])
                            if debug:
                                print(f"{p}: summary rows: {summary}")
                        else:
                            summary = match[1]
                            if debug:
                                print(f"{p}: summary cols: {summary}")
                        # Add this summary to the sum of summaries
                        sum_of_summaries += summary
                        # We only need to find 1 reflection per list of items
                        break
    print(f"sum of summaries: {sum_of_summaries}")
    return sum_of_summaries

# In each pattern, fix the smudge and find the different line of reflection.
# What number do you get after summarizing the new reflection line in each pattern in your notes?
def part_two(data=data):
    ...

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
