from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
import operator
from functools import reduce

# What day and year is this solution for?
day = 2
year = 2023

# Game globals
max_cubes = { "red": 12, "green": 13, "blue": 14 }

# Sample game data:
# Game 1: 4 green, 2 blue; 1 red, 1 blue, 4 green; 3 green, 4 blue, 1 red; 7 green, 2 blue, 4 red; 3 red, 7 green; 3 red, 3 green
# Game 2: 1 blue, 11 red, 1 green; 3 blue, 2 red, 4 green; 11 red, 2 green, 2 blue; 13 green, 5 red, 1 blue; 4 green, 8 red, 3 blue
raw = aoc_helper.fetch(day, year)

# Parse the game data into a list of tuples where the max of each color of cube is stored per game
def parse_raw(raw: str):
    lines = raw.splitlines()
    data = list()
    for game, line in enumerate(lines,1):
        red = list(map(int, re.findall(r"(\d+) red", line)))
        green = list(map(int, re.findall(r"(\d+) green", line)))
        blue = list(map(int, re.findall(r"(\d+) blue", line)))
        data.append((max(red), max(green), max(blue)))
    return data

data = parse_raw(raw)

# Determine which games would have been possible if the bag had been loaded with only
# 12 red cubes, 13 green cubes, and 14 blue cubes.
# What is the sum of the IDs of those games?
def part_one(data=data):
    sum_game_ids = 0
    for game_id, game in enumerate(data,1):
        if game[0] <= max_cubes["red"] and game[1] <= max_cubes["green"] and game[2] <= max_cubes["blue"]:
            sum_game_ids += game_id
    print(f"sum_game_ids: {sum_game_ids}")
    return sum_game_ids

# For each game, find the minimum set of cubes that must have been present.
# What is the sum of the power of these sets?
def part_two(data=data):
    sum_game_cube_powers = 0
    for game_id, game in enumerate(data,1):
        sum_game_cube_powers += reduce(operator.mul, game, 1)
    print(f"sum_game_cube_powers: {sum_game_cube_powers}")
    return sum_game_cube_powers

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
