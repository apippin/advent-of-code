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

raw = aoc_helper.fetch(1, 2022)

def parse_raw(raw: str):
    lines = raw.splitlines()
    return lines


data = parse_raw(raw)

# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
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

aoc_helper.lazy_test(day=1, year=2022, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    calories = part_one(data)
    max_calories = calories[0]+calories[1]+calories[2]
    print(f"P2: Max calories: {max_calories}")

aoc_helper.lazy_test(day=1, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=1, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=1, year=2022, solution=part_two, data=data)
