from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
import itertools as it
from math import lcm

# What day and year is this solution for?
day = 8
year = 2023

# Sample game data:
# RL
#
# AAA = (BBB, CCC)
# BBB = (DDD, EEE)
# CCC = (ZZZ, GGG)
# DDD = (DDD, DDD)
# EEE = (EEE, EEE)
# GGG = (GGG, GGG)
# ZZZ = (ZZZ, ZZZ)
raw = aoc_helper.fetch(day, year)

# Parse out the steps and nodes and store them in a dictionary
def parse_raw(raw: str):
    lines = raw.splitlines()
    steps = list(lines[0])
    data = dict()
    data["steps"] = steps
    for line in lines[2:]:
        nodes = (re.findall(r"(\w+)", line))
        data[nodes[0]] = (nodes[1], nodes[2])
    return data

# Parse the game data
data = parse_raw(raw)

# Find the number of steps to get from the given node to an ending node
def path_finder(data, node):
    num_steps = 0
    #print(f"starting from {node}")
    for step in it.cycle(data['steps']):
        #print(f"step: {step}")
        num_steps += 1
        match step:
            case 'L':
                node = data[node][0]
            case 'R':
                node = data[node][1]
        #print(f"next_node: {node}")
        if node.endswith('Z'):
            #print(f"found path with num_steps: {num_steps}")
            return num_steps

# Starting at AAA, follow the left/right instructions.
# How many steps are required to reach ZZZ?
def part_one(data=data):
    #print(f"{data}")
    num_steps = path_finder(data, 'AAA')
    print(f"num_steps: {num_steps}")
    return num_steps

# Simultaneously start on every node that ends with A.
# How many steps does it take before you're only on nodes that end with Z?
def part_two(data=data):
    starting_nodes = [x for x in data.keys() if x.endswith('A')]
    #print(f"{starting_nodes}")
    # Paths are cyclic so navigating them all together takes a really long time (mine never finished).
    # So let's do this mathematically by first finding the steps per path to each end node, and then taking the LCM of those.
    # The LCM will be the number of steps for each path to get to an end node, because it is the least common mulitple of each path length.
    # The LCM is the lowest number that is a multiple of each path's steps to get to a node ending in Z.
    lcms = [path_finder(data, node) for node in starting_nodes]
    num_steps = lcm(*lcms)
    print(f"num_steps: {num_steps}")
    return num_steps

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
