from collections import defaultdict, deque
from typing import TYPE_CHECKING

import aoc_helper
from aoc_helper import (
    Grid,
    PrioQueue,
    SparseGrid,
    decode_text,
    extract_ints,
    extract_iranges,
    extract_ranges,
    extract_uints,
    frange,
    irange,
    iter,
    list,
    map,
    range,
    search,
    tail_call,
)

import re
import operator
from functools import reduce

from collections import defaultdict
def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))

max_cubes = { "red": 12, "green": 13, "blue": 14 }

raw = aoc_helper.fetch(2, 2023)

def parse_raw(raw: str):
    lines = raw.splitlines()
    data = nested_dict(3, int)
    for line in lines:
        match = re.search(r"Game (\d+):", line)
        game = int(match.group(1))
        line = line.replace(f"Game {game}: ","")
        game_sets = line.split(";")
        for set_num, game_set in enumerate(game_sets):
            cubes = game_set.split(",")
            for cube in cubes:
                match = re.search(r"(\d+) (\w+)", cube)
                data[game][set_num][match.group(2)] = int(match.group(1))
    return data

data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    sum_game_ids = 0
    for game in data.keys():
        game_possible=True
        for set_num in data[game].keys():
            for color in data[game][set_num].keys():
                print(f"game: {game} set: {set_num} color: {color} num: {data[game][set_num][color]}")
                if data[game][set_num][color] > max_cubes[color]:
                    game_possible=False
        if game_possible:
            sum_game_ids += game
    return sum_game_ids

aoc_helper.lazy_test(day=2, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    sum_game_cube_powers = 0
    for game in data.keys():
        game_min_cubes = { "red": 0, "green": 0, "blue": 0 }
        for set_num in data[game].keys():
            for color in data[game][set_num].keys():
                print(f"game: {game} set: {set_num} color: {color} num: {data[game][set_num][color]}")
                if data[game][set_num][color] > game_min_cubes[color]:
                    game_min_cubes[color] = data[game][set_num][color]
        sum_game_cube_powers += reduce(operator.mul, list(game_min_cubes.values()), 1)
    return sum_game_cube_powers


aoc_helper.lazy_test(day=2, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=2, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=2, year=2023, solution=part_two, data=data)
