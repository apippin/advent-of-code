from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
import difflib

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

# Determine if strings differ by only 1 character
def strings_differ_by_1(string1, string2):
    if len(string1) == len(string2):
        count_diffs = 0
        for a, b in zip(string1, string2):
            if a!=b:
                if count_diffs: return False
                count_diffs += 1
        return True
    return False

# Find all the consecutive item pairs and return the list of them
def find_adjacents(p, items):
    adjacents = []
    for i, a in enumerate(items):
        if (i+1 < len(items)):
            adjacents.append((i, i+1))
    return (adjacents)

# Find all the consecutive item pairs that match each other and return the list of them
def find_adjacent_matches(p, items):
    matches = []
    fixed_smudge = False
    for i, a in enumerate(items):
        if (i+1 < len(items)) and (items[i] == items[i+1]):
            matches.append((i, i+1))
    return (matches, fixed_smudge)

# Compare the 2 strings to identify if a single character can be changed to cause them to match
# If you can find one, it's called a smudge, and should be changed so they match
def find_smudge(p, a, b, item_a, item_b, items_c):
    if debug:
        print(f"{p}: finding smudge in a:{a} b:{b} item_a:{item_a} item_b:{item_b}")
    fixed_smudge = False
    if strings_differ_by_1(item_a, item_b):
        fixed_smudge = True
        # Find the location and character that is different
        items_a_l = list(item_a)
        items_b_l = list(item_b)
        diffs = [i for i, x in enumerate(zip(items_a_l,items_b_l)) if x[0]!=x[1]]
        diff_loc = diffs[0]
        old_c = item_a[diff_loc]
        new_c = item_b[diff_loc]
        # Update the item
        item_a = item_b
        if debug:
            print(f"{p}: fixed smudge in item_a[{a}]:{item_a} by changing {old_c} to {new_c} in pos {diff_loc}")
        # Update the other item (in rows or cols)
        items_c_l = list(items_c[diff_loc])
        items_c_l[a] = new_c
        items_c[diff_loc] = "".join(items_c_l)
        if debug:
            print(f"{p}: fixed smudge in item_c[{diff_loc}]:{items_c[diff_loc]} by changing {old_c} to {new_c} in pos {a}")
    return (item_a, item_b, items_c, fixed_smudge)

# Find the line of reflection in each of the patterns in your notes.
# What number do you get after summarizing all of your notes?
def part_one(data=data, part_two=False):
    #print(f"{data}")
    sum_of_summaries = 0
    for p,pattern in enumerate(data,1):
        fixed_smudge = False
        rows = pattern["rows"]
        rows_orig = rows[:]
        cols = pattern["cols"]
        cols_orig = cols[:]
        if debug:
            print(f"{p}: rows:")
            print(*rows,sep='\n')
            print(f"{p}: cols:")
            print(*cols,sep='\n')
        for items in (rows, cols):
            if items == rows:
                items_name = "rows"
                other_items = cols
            else:
                items_name = "cols"
                other_items = rows
            # Find all of the adjacent matches in this list of items
            #adjacent_matches = find_adjacent_matches(p, items)
            adjacent_matches = find_adjacents(p, items)
            # Go through each adjacent_matches while we haen't found a reflection and we still have adjacent matches to check
            summary = 0
            for match in adjacent_matches:
                if debug:
                    print(f"{p}: {items_name} match: {match}")
                if match[0] >= 0:
                    a = match[0]
                    b = match[1]
                    if part_two and not fixed_smudge and a >= 0 and b <len(items) and items[a] != items[b]:
                        # If we find a smudge, we need to fix it in both rows and cols since I've stored these as 2 different data structures
                        (items[a], items[b], other_items, fixed_smudge) = find_smudge(p, a, b, items[a], items[b], other_items)
                    while (a >= 0 and b < len(items)) and (items[a] == items[b]):
                        a -= 1
                        b += 1
                        if part_two and not fixed_smudge and a >= 0 and b <len(items) and items[a] != items[b]:
                            # If we find a smudge, we need to fix it in both rows and cols since I've stored these as 2 different data structures
                            (items[a], items[b], other_items, fixed_smudge) = find_smudge(p, a, b, items[a], items[b], other_items)
                    # If either edge hit a boundary and we still matched, we found a valid reflection
                    if debug:
                        print(f"{p}: a:{a} b:{b} items:{len(items)}")
                    if a < 0 or b >= len(items):
                        if items_name == "rows":
                            summary = 100 * (match[1])
                            print(f"{p}: summary rows: {summary}")
                        else:
                            summary = match[1]
                            print(f"{p}: summary cols: {summary}")
                        # Add this summary to the sum of summaries
                        sum_of_summaries += summary
                        # We only need to find 1 reflection per list of items
                        break
                    else:
                        # Since we didn't find a valid reflection, undo it here
                        if fixed_smudge:
                            if debug:
                                print(f"{p}: Undid fixed smudge")
                            rows = rows_orig[:]
                            cols = cols_orig[:]
                            fixed_smudge = False
            # We only need to find the first reflection in the pattern (rows then cols)
            if summary != 0:
                break
    print(f"sum of summaries: {sum_of_summaries}")
    return sum_of_summaries

# You discover that every mirror has exactly one smudge: exactly one . or # should be the opposite type.
# In each pattern, you'll need to locate and fix the smudge that causes a different reflection line to be valid.
# (The old reflection line won't necessarily continue being valid after the smudge is fixed.)
# In each pattern, fix the smudge and find the different line of reflection.
# What number do you get after summarizing the new reflection line in each pattern in your notes?
def part_two(data=data):
    return part_one(data, True)

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
