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
part_two_flag = False

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
        if part_two_flag:
            # The color is actually #DistDir with the dir being the last number, and dist being hex coded distance
            color_dir = re.findall(r'[0-9A-Fa-f]+', color, re.I)[-1]
            dir = color_dir[-1] # Last digit is the direction
            dist = int(color_dir[:-1],16) # All others are the distance as a hex number
        match dir:
            case 'R' | '0':
                dir = (0,1)
            case 'L' | '2':
                dir = (0,-1)
            case 'D' | '1':
                dir = (1,0)
            case 'U' | '3':
                dir = (-1,0)
        data.append((dir,dist,color))
    return data

# Parse the game data
data = parse_raw(raw)

# send a numpy array of (x,y) cordinates as an argument and use the shoelace method to get the area
def shoelace(x_y):
    x_y = np.array(x_y)
    x_y = x_y.reshape(-1,2)

    x = x_y[:,0]
    y = x_y[:,1]

    S1 = np.sum(x*np.roll(y,-1))
    S2 = np.sum(y*np.roll(x,-1))

    area = .5*np.absolute(S1 - S2)

    return area

def dig(data):
    # We will store our dig site as a list of list (defaultlist to autofill missing points with 0)
    dig_site = defaultlist(lambda:defaultlist(int))
    # We need to store the vertices to give to the shoelace alogorithm to calculate the linear area
    vertices = []
    # Dig our starting position in the middle of an area big enough to hold the entire dig plan
    x = 1000
    y = 1000
    vertices.append((x,y))
    perim = 0
    # Dig all the other positions based on our dig plan
    for dig_plan in data:
        dist = int(dig_plan[1])-1
        if dig_plan[0][0] > 0:
            dy = dig_plan[0][0] + dist
            y += dy
            perim += abs(dy)
        elif dig_plan[0][0] < 0:
            dy = dig_plan[0][0] - dist
            y += dy
            perim += abs(dy)
        if dig_plan[0][1] > 0:
            dx = dig_plan[0][1] + dist
            x += dx
            perim += abs(dx)
        elif dig_plan[0][1] < 0:
            dx = dig_plan[0][1] - dist
            x += dx
            perim += abs(dx)
        #print(f"dug: ({y},{x})")
        vertices.append((x,y))
    #print(*vertices, sep='\n')
    #print(f"perim: {perim}")
    # The shoelace returns the linear area (not including the perimeter line)
    # So we need to add in the perimeter (divided by 2) + 1 full rotation
    return(int(shoelace(vertices)) + (perim//2) + 1)

# The Elves are concerned the lagoon won't be large enough;
# if they follow their dig plan, how many cubic meters of lava could it hold?
def part_one(data=data):
    #print(*data, sep='\n')
    cubic_meters = dig(data)
    print(f"cubic_meters: {cubic_meters}")
    return cubic_meters

# Convert the hexadecimal color codes into the correct instructions;
# if the Elves follow this new dig plan, how many cubic meters of lava could the lagoon hold?
def part_two(data=data):
    #print(*data, sep='\n')
    cubic_meters = dig(data)
    print(f"cubic_meters: {cubic_meters}")
    return cubic_meters

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
part_two_flag = True
data = parse_raw(raw) # reparse the data in joker card variant mode
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
