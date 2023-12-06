from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
import math
import numpy as np

# What day and year is this solution for?
day = 6
year = 2023

# Sample game data:
# Time:      7  15   30
# Distance:  9  40  200
raw = aoc_helper.fetch(day, year)

def parse_raw(raw: str):
    lines = raw.splitlines()
    data = dict()
    data["time"] = tuple(map(int, re.findall(r"(\d+)", lines[0])))
    data["distance"] = tuple(map(int, re.findall(r"(\d+)", lines[1])))
    return data

# Parse the game data
data = parse_raw(raw)

# Calculate the number of ways you can win a race
# Do this by solving these equations:
# velocity*time = distance =>
# holdTime + travelTime = totalTime =>
# distance = holdTime*(totalTime - holdTime) =>
# -holdTime^2 + totalTime*holdTime - distance > 0 (solve for holdTime)
def calc_ways(data, race, time, distance):
    # quadratic:-x^2 + Tx - D = 0
    coeff = [-1, time, -distance]
    roots = np.roots(coeff) # get the roots of the quadratic equation above
    hold_min = math.floor(roots[1].real)+1
    hold_max = time - hold_min
    ways = hold_max - hold_min + 1
    #print(f"time={time} distance={distance} hold_min={hold_min} hold_max={hold_max} ways={ways}")
    return ways

# Determine the number of ways you could beat the record in each race.
# What do you get if you multiply these numbers together?
def part_one(data=data):
    #print(f"{data}")
    product_of_ways = 1
    for race in range(0,len(data["time"])):
        time = data["time"][race]
        distance = data["distance"][race]
        product_of_ways *= calc_ways(data, race, time, distance)
    print(f"product of ways: {product_of_ways}")
    return product_of_ways

# There's really only one race - ignore the spaces between the numbers on each line.
def part_two(data=data):
    time = int(''.join([str(x) for x in data["time"]]))
    distance = int(''.join([str(x) for x in data["distance"]]))
    ways = calc_ways(data, 0, time, distance)
    print(f"ways: {ways}")
    return ways

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
