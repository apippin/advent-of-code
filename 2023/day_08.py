from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re

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

# Parse out the steps and nodes
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

# Starting at AAA, follow the left/right instructions.
# How many steps are required to reach ZZZ?
def part_one(data=data):
    #print(f"{data}")
    node = 'AAA'
    num_steps = 0
    while(node != 'ZZZ'):
        for step in data["steps"]:
            match step:
                case 'L':
                    node = data[node][0]
                case 'R':
                    node = data[node][1]
            #print(f"next_step: {node}")
            num_steps += 1
    print(f"num_steps: {num_steps}")
    return num_steps

# Simultaneously start on every node that ends with A.
# How many steps does it take before you're only on nodes that end with Z?
def path_finder(node):
    pass

def part_two(data=data):
    #print(f"{data}")
    num_steps = 0
    nodes = [x for x in data.keys() if x.endswith('A')]
    #print(f"starting_nodes: {nodes}")
    while(len([x for x in nodes if x.endswith('Z')]) != len(nodes)):
        for step in data['steps']:
            #print(f"step: {step}")
            new_nodes = list()
            for node in nodes:
                #print(f"node: {node}")
                match step:
                    case 'L':
                        new_nodes.append(data[node][0])
                    case 'R':
                        new_nodes.append(data[node][1])
            num_steps += 1
            nodes = new_nodes
            #print(f"next_step: {nodes}")
    print(f"num_steps: {num_steps}")
    return num_steps

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
