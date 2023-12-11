from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re

# What day and year is this solution for?
day = 10
year = 2023

# Sample game data:
"""
F - 7
|   |
L - J
"""
raw = aoc_helper.fetch(day, year)

# ...
def parse_raw(raw: str):
    lines = raw.splitlines()
    data = []
    for i, line in enumerate(lines):
        data.append(list(line))
    return data

# Parse the game data
data = parse_raw(raw)

def parse_map(data):
    start = None

    # Find our starting location
    for i, line in enumerate(data):
        if "S" in line:
            # Store the row, col of the start location
            start = (i, line.index("S"))
    #print(f"start: {start}")

    """ four adjacent directions """
    adj_dirs = [  # top, right, bottom, left
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]

    """ define the direction connected to the adjacent node for each symbol """
    sym_connects = {  # top, right, bottom, left
        "|": (1, 0, 1, 0),
        "-": (0, 1, 0, 1),
        "L": (1, 1, 0, 0),
        "J": (1, 0, 0, 1),
        "7": (0, 0, 1, 1),
        "F": (0, 1, 1, 0),
    }

    """ define the types of adjacent nodes that can be connected for each direction """
    adj_connect_types = {
        (-1, 0): "F|7",
        (0, 1): "7-J",
        (1, 0): "L|J",
        (0, -1): "F-L",
    }

    # Set each location to a 1 if its adjacent tile is one we can connect to
    # We need to convert the starting symbol into its connection symbol
    adjs = [0, 0, 0, 0]  # top, right, bottom, left
    # Check all adjacent locations to our starting position
    for i, adj in enumerate(adj_dirs):
        # Create a (row, col) tuple of the adjacent location
        pos = tuple(a + b for a, b in zip(start, adj))
        # If the data at the adjacent row or col is a type we can connect to, add it to our adjacency list
        if data[pos[0]][pos[1]] in adj_connect_types[adj]:
            adjs[i] = 1
    #print(f"start: {start}")
    #print(f"adjs: {adjs}")
    data[start[0]][start[1]] = list(sym_connects.keys())[list(sym_connects.values()).index(tuple(adjs))]
    #print(f"{data}")

    # Keep track of a queue of nodes we need to visit
    queue = [start]
    # Keep track of the nodes we have visited
    visited = set()

    while queue:
        pos = queue.pop(0)
        # We don't need to do anything if we have already visited this node
        if pos in visited:
            continue
        visited.add(pos)
        # We don't need to do anything if the node is not a valid pipe piece
        if data[pos[0]][pos[1]] in " .":
            continue
        # Get the symbol at this position
        sym = data[pos[0]][pos[1]]
        _dirs = [adj_dirs[i] for i, v in enumerate(sym_connects[sym]) if v == 1]
        # We need to append the next position we need to check
        for dy, dx in _dirs:
            queue.append((pos[0] + dy, pos[1] + dx))

    return visited

# Find the single giant loop starting at S.
# How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?
def part_one(data=data):
    visited = parse_map(data)
    steps = len(visited) // 2
    print(f"steps_to_farthest_position: {steps}")
    return steps

# Figure out whether you have time to search for the nest by calculating the area within the loop.
# How many tiles are enclosed by the loop?
def part_two(data=data):
    visited = parse_map(data)
    enclosed = []

    # For each row in our data
    for row, items in enumerate(data):
        # For each column in each row, replace the tile with a "." if it isn't part of our loop
        line = [v if (row, col) in visited else "." for col, v in enumerate(items)]
        # Turn our list of chars into a string
        line = "".join(line)
        # Replace all the pipes in our loop with vertical bars.
        # You can use a flag to determine whether you're inside or outside of the loop when crossing a pipe,
        # count the tiles only when you're inside the loop. when encountering L-*J and F-*7 patterns,
        # consider it as jumping over 2 pipes. conversely, when encountering L-*7 and F-*J,
        # consider it as jumping over only 1 pipe
        line = re.sub(r"L-*7", "|", line)
        line = re.sub(r"L-*J", "||", line)
        line = re.sub(r"F-*7", "||", line)
        line = re.sub(r"F-*J", "|", line)
        #print(f"{line}")

        # Keep track of how many pipes we have crossed
        # An odd number means we are inside our pipe loop
        # An even number means we are outside our pipe loop
        cross = 0
        # Keep track of how many tiles are inside our pipe loop
        inside = 0

        # For each symbol in the line:
        for c in line:
            # If the symbol is blank or if we haven't crossed 2 pipes, count it as an inside tile
            if c == "." and cross % 2:
                inside += 1
            # If we cross a pipe, increment our cross counter
            elif c in "|":
                cross += 1
        enclosed.append(inside)

    print(f"tiles_enclosed_by_loop: {sum(enclosed)}")
    return sum(enclosed)

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Reparse the game data (since we change in in part_one)
data = parse_raw(raw)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
