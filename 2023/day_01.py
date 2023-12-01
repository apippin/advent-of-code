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
from word2number import w2n

raw = aoc_helper.fetch(1, 2023)


def parse_raw(raw: str):
    lines = raw.splitlines()
    return lines


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    sum = 0
    for line in data:
        numbers = re.findall(r'(\d)', line)
        if len(numbers) == 1:
            numbers.append(numbers[0])
        number = f"{numbers[0]}{numbers[-1]}"
        sum += int(number)
        #print(f"line: {line} numbers: {numbers} number: {number} sum: {sum}")
    print(f"calibration sum: {sum}")
    return sum
        


aoc_helper.lazy_test(day=1, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    sum = 0
    for line in data:
        match = re.search(r'(\d|one|two|three|four|five|six|seven|eight|nine)', line)
        first = match.group(0)
        match = re.search(r'.*(\d|one|two|three|four|five|six|seven|eight|nine)', line)
        last = match.group(1)
        if not first.isnumeric():
            first = w2n.word_to_num(first)
        if not last.isnumeric():
            last = w2n.word_to_num(last)
        number = f"{first}{last}"
        sum += int(number)
        #print(f"line: {line} number: {number} sum: {sum}")
    print(f"corrected calibration sum: {sum}")
    return sum

#part_two(data)

aoc_helper.lazy_test(day=1, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=1, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=1, year=2023, solution=part_two, data=data)
