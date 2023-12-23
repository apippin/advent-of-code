from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
from defaultlist import defaultlist
import numpy as np

# What day and year is this solution for?
day = 18
year = 2023

# Game globals
...

# Sample game data:
"""
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
raw = aoc_helper.fetch(day, year)

# Create a list of tuples from each line of input (direction, distance, color)
def parse_raw(raw: str):
    lines = raw.splitlines()
    data = []
    for line in lines:
        (dir,dist,color) = line.split(' ')
        match dir:
            case 'R':
                dir = (0,1)
            case 'L':
                dir = (0,-1)
            case 'D':
                dir = (1,0)
            case 'U':
                dir = (-1,0)
        data.append((dir,dist,color))
    return data

# Parse the game data
data = parse_raw(raw)

# The Elves are concerned the lagoon won't be large enough;
# if they follow their dig plan, how many cubic meters of lava could it hold?
def part_one(data=data):
    dig_site = defaultlist(lambda:defaultlist(int))
    #print(*data, sep='\n')
    # Dig our starting position
    x = 50
    y = 500
    dig_site[x][y] = 1 # Starting location is dug
    # Dig all the other positions based on our dig plan
    for dig_plan in data:
        for dist in range(int(dig_plan[1])):
            y += dig_plan[0][0]
            x += dig_plan[0][1]
            #print(f"dug: ({y},{x})")
            dig_site[y][x] = 1
    #print(*dig_site, sep='\n')
    for y in dig_site:
        print(*y, sep='')

    # Dig out the interior
    for y,row in enumerate(dig_site):
        dig_it = False
        for x,dug in enumerate(row):
            #print(f"y: {y} x: {x} dug: {dug} dig_it: {dig_it}")
            if dig_site[y][x] == 1 and (x < len(row)-1) and (dig_site[y][x+1] == 0):
                dig_it = not dig_it
            elif dig_it:
                dig_site[y][x] = 1
    #print(*dig_site, sep='\n')
    for y in dig_site:
        print(*y, sep='')

    cubic_meters = sum(sum(dig_site,[]))
    print(f"cubic_meters: {cubic_meters}")
    return cubic_meters

# ...
def part_two(data=data):
    ...

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
#aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
#aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
#aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
