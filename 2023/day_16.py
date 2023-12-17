from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re

# What day and year is this solution for?
day = 16
year = 2023

# Game globals
...

# Sample game data:
"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
raw = aoc_helper.fetch(day, year)

# Store each location in a 2d array with its symbol read from the input: data = [[]]
def parse_raw(raw: str):
    lines = raw.splitlines()
    return [list(c) for c in lines]

# Parse the game data
data = parse_raw(raw)

# Given the starting position of the beam, see how many spaces are energized
def follow_beam(data, starting_loc):
    # Create a parallel energized set of (x,y) tuples as we visit each coordinate.
    energized = set()
    # Create a seen set of (x,y,dx,dy) tuples we have already seen or visited to catch cycles.
    seen = set()
    # Use a stack to push on nodes to visit, start with (0,0,1,0)
    # x,y = current coordinates dx=change to get next x coordinate, dy=change to get next y coordinate
    # Since we start in the top-left corner and we start by heading right (dx=1)
    stack = [starting_loc]
    # While we still have spaces to visit
    while stack:
        x, y, dx, dy = stack.pop()
        # As long as that location is still on our grid, and our next locations are too:
        while 0 <= x < len(data[0]) and 0 <= y < len(data):
            # If (x,y,dx,dy) is already in seen (we're already been here), break
            if (x,y,dx,dy) in seen:
                break
            # Add location to seen and energized sets
            seen.add((x,y,dx,dy))
            energized.add((x,y))
            #print(f"visiting: [{x}][{y}]:{data[x][y]} with dx:{dx} dy:{dy}")
            # match on each symbol in a case statement to act on each differently
            # append new locations to the stack if the symbol causes us to fork off a new beam
            # otherwise, just update x,y,dx,dy accordingly
            match data[y][x]:
                # We hit an empty space
                case '.':
                    # Keep moving in the direction we were already going
                    x += dx
                    y += dy
                # We hit a horizontal splitter
                case '-':
                    if dx:
                        # Keep going in the direction we were going
                        x += dx
                    else:
                        # We need to explore a new direction to the left
                        stack.append((x-1, y, -1, 0))
                        # We need to explore a new direction to the right
                        stack.append((x+1, y, 1, 0))
                        # Go onto the next location in our stack
                        break
                # We hit a vertical splitter
                case '|':
                    if dy:
                        # Keep going in the direction we were going
                        y += dy
                    else:
                        # We need to explore a new direction up
                        stack.append((x, y-1, 0, -1))
                        # We need to explore a new direction down
                        stack.append((x, y+1, 0, 1))
                        # Go onto the next location in our stack
                        break
                # We hit a corner mirror
                case '/':
                    # if we were moving down when we hit it, go left
                    if dy == 1:
                        dx, dy = -1,0
                        x += dx
                    # if we were moving up when we hit it, go right
                    elif dy == -1:
                        dx, dy = 1,0
                        x += dx
                    # if we were moving right when we hit it, go up
                    elif dx == 1:
                        dx, dy = 0,-1
                        y += dy
                    # if we were moving left when we hit it, go down
                    elif dx == -1:
                        dx, dy = 0,1
                        y += dy
                # We hit a corner mirror
                case '\\':
                    # if we were moving down when we hit it, go right
                    if dy == 1:
                        dx, dy = 1,0
                        x += dx
                    # if we were moving up when we hit it, go left
                    elif dy == -1:
                        dx, dy = -1,0
                        x += dx
                    # if we were moving right when we hit it, go down
                    elif dx == 1:
                        dx, dy = 0,1
                        y += dy
                    # if we were moving left when we hit it, go up
                    elif dx == -1:
                        dx, dy = 0,-1
                        y += dy
    return len(energized)

# The light isn't energizing enough tiles to produce lava; to debug the contraption,
# you need to start by analyzing the current situation.
# With the beam starting in the top-left heading right, how many tiles end up being energized?
def part_one(data=data):
    #print(*data, sep="\n")
    energized = follow_beam(data, (0,0,1,0))
    print(f"num_energized: {energized}")
    return energized

# Find the initial beam configuration that energizes the largest number of tiles;
# How many tiles are energized in that configuration?
def part_two(data=data):
    #print(*data, sep="\n")
    energized = []
    for x in range(0,len(data[0])):
        for y in range(0,len(data)):
            #print(f"x: {x} y: {y}")
            # top left corner
            if x == 0 and y == 0:
                energized.append(follow_beam(data, (x,y,1,0))) # right
                energized.append(follow_beam(data, (x,y,0,1))) # down
            # top right corner
            if x == len(data[0])-1 and y == 0:
                energized.append(follow_beam(data, (x,y,-1,0))) # left
                energized.append(follow_beam(data, (x,y,0,1))) # down
            # bottom right corner
            if x == len(data[0])-1 and y == len(data)-1:
                energized.append(follow_beam(data, (x,y,-1,0))) # left
                energized.append(follow_beam(data, (x,y,0,-1))) # up
            # bottom left corner
            if x == 0 and y == len(data)-1:
                energized.append(follow_beam(data, (x,y,1,0))) # right
                energized.append(follow_beam(data, (x,y,0,-1))) # up
            # top edge
            if y == 0:
                energized.append(follow_beam(data, (x,y,0,1))) # down
            # right edge
            if x == len(data[0])-1:
                energized.append(follow_beam(data, (x,y,-1,0))) # left
            # bottom edge
            if y == len(data)-1:
                energized.append(follow_beam(data, (x,y,0,-1))) # up
            # left edge
            if x == 0:
                energized.append(follow_beam(data, (x,y,1,0))) # right

    print(f"num_energized: {max(energized)}")
    return max(energized)

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
