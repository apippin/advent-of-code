from collections import defaultdict, deque
from typing import TYPE_CHECKING

import aoc_helper

# What day and year is this solution for?
day = 1
year = 2022

# Sample Data
# This list represents the Calories of the food carried by five Elves:
# 1000
# 2000
# 3000
# 
# 4000
#
# 5000
# 6000
#
# 7000
# 8000
# 9000
# 
# 10000
raw = aoc_helper.fetch(1, 2022)

def parse_raw(raw: str):
    lines = raw.splitlines()
    return lines

data = parse_raw(raw)

# Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
def part_one(data=data):
    calories = []
    elf = 0
    calories.append(0)
    for line in data:
        #print(f"elf: {elf} line: {line}")
        if not line.strip():
            elf += 1
            calories.append(0)
        else:
            calories[elf] += int(line)
    calories.sort(reverse=True)
    max_calories = calories[0]
    print(f"P1: Max calories: {max_calories}")
    return calories

# Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?
def part_two(data=data):
    calories = part_one(data)
    max_calories = calories[0]+calories[1]+calories[2]
    print(f"P2: Max calories: {max_calories}")

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
