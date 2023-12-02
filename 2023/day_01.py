from collections import defaultdict, deque
from typing import TYPE_CHECKING

import aoc_helper
import re
from word2number import w2n

# What day and year is this solution for?
day = 1
year = 2023

# Sample game data:
# 1abc2
# pqr3stu8vwx
# a1b2c3d4e5f
# treb7uchet
raw = aoc_helper.fetch(1, 2023)

def parse_raw(raw: str):
    lines = raw.splitlines()
    return lines

data = parse_raw(raw)

# On each line, the calibration value can be found by combining the first digit and 
# the last digit (in that order) to form a single two-digit number.
# What is the sum of all of the calibration values?
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

# It looks like some of the digits are actually spelled out with letters: 
# one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".
# Equipped with this new information, you now need to find the real first and last digit on each line.
# What is the sum of all of the calibration values?
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

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
