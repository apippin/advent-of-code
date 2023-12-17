from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
import numpy as np

# What day and year is this solution for?
day = 14
year = 2023

# Sample game data:
"""
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
raw = aoc_helper.fetch(day, year)

# Parse the rows of data into a list of chars
def parse_raw(raw: str):
    lines = raw.splitlines()
    return [list(r) for r in lines]

# Parse the game data
data = parse_raw(raw)

# Roll rocks
def roll_rocks(data, direction):

    #print(f"{direction}:")
    #print(*data, sep="\n")
    #print("\n")

    new_data = data.copy()

    if direction == 'N' or direction == 'S':
        new_data = data.T

    for rocks in new_data:
        # Keep moving the rocks until we can't move them anymore
        first = True
        if direction == 'S' or direction == 'E':
            rocks = np.flip(rocks)
        #print(f"0: {rocks}")
        while first or not np.array_equal(rocks, last_rocks):
            first = False
            last_rocks = rocks.copy()
            for r,rock in enumerate(rocks):
                # Look for an empty space followed by a round rock
                # If you find one, swap their positions
                if r < len(rocks)-1 and rocks[r] == '.' and rocks[r+1] == 'O':
                    rocks[r] = 'O'
                    rocks[r+1] = '.'
        if direction == 'S' or direction == 'E':
            rocks = np.flip(rocks)
        #print(f"1: {rocks}")

    if direction == 'N' or direction == 'S':
        data = new_data.T
    else:
        data = new_data

    #print(f"{direction}:")
    #print(*data, sep="\n")
    return data

def calc_load(data):
    total_load = 0
    for r,row in enumerate(data):
        row_load = len(data) - r
        load = (row == 'O').sum() * row_load
        total_load += load
        #print(f"{r}: {row} {row_load} {load}")
    return total_load

# Tilt the platform so that the rounded rocks all roll north.
# Afterward, what is the total load on the north support beams?
def part_one(data=data):
    data = np.array(data)
    #print(*data, sep="\n")
    data = roll_rocks(data, "N")
    total_load = calc_load(data)
    print(f"total_load: {total_load}")
    return total_load

# Run the spin cycle for 1000000000 cycles.
# Afterward, what is the total load on the north support beams?
def part_two(data=data):
    data = np.array(data)
    #print(*data, sep="\n")
    # Roll the rocks
    load_history = []
    for i in range(0, 1_000_000_000):
        #print(f"Iteration {i}")
        data = roll_rocks(data, "N")
        data = roll_rocks(data, "W")
        data = roll_rocks(data, "S")
        data = roll_rocks(data, "E")
        load_history.append(calc_load(data))

        for cycle_size in range(2,100):
            cycle = load_history[-cycle_size:]
            if load_history[-cycle_size*2:-cycle_size] == cycle:  # cycle found
                mysterious_offset = -2  # not quite about this one to be honest...
                remaining_iterations = 1_000_000_000 - i + mysterious_offset
                total_load = cycle[remaining_iterations % cycle_size]
                #print(f"{load_history}")
                print(f"total_load: {total_load}")
                return total_load

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
