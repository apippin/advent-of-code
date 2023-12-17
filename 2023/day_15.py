from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re

# What day and year is this solution for?
day = 15
year = 2023

# Sample game data:
# rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
raw = aoc_helper.fetch(day, year)

# remove all newlines and split the raw input on commas and return as a list
def parse_raw(raw: str):
    return raw.strip().split(',')

# Parse the game data
data = parse_raw(raw)

# Run the HASH algorithm on the given step
def get_hash_value(data, step):
    # For each character in each step
    current_value = 0
    for ch in step:
        # Convert the character into its ASCII code
        ascii_code = ord(ch)
        # Increase current_value by its ASCII code
        current_value += ascii_code
        # Set the current_value to itself multiplied by 17
        current_value *= 17
        # Set the current value to the remainder of dividing itself by 256
        current_value %= 256
        #print(f"{s}: {ch} {current_value}")
    return current_value

# Run the HASH algorithm on each step in the initialization sequence.
# What is the sum of the results? (The initialization sequence is one long line; be careful when copy-pasting it.)
def part_one(data=data):
    #print(*data, sep="\n")
    # For each step
    sum_of_results = 0
    for s,step in enumerate(data):
        current_value = get_hash_value(data, step)
        #print(f"{s}: {step} {current_value}")
        sum_of_results += current_value
    print(f"sum_of_results: {sum_of_results}")
    return sum_of_results

# With the help of an over-enthusiastic reindeer in a hard hat,
# follow the initialization sequence.
# What is the focusing power of the resulting lens configuration?
def part_two(data=data):
    #print(*data, sep="\n")
    boxes = {}
    for step in data:
        match = re.search('(\w+)([=-]+)(\d*)',step)
        label = match[1]
        box = get_hash_value(data, label)
        operation = match[2]
        focal_length = match[3]
        #print(f"step: {step} box: {box} operation: {operation} focal_length: {focal_length}")
        if operation == '=':
            if box not in boxes:
                boxes[box] = [[label, focal_length]]
                #print(f"={boxes}")
            else:
                for label_in_box in boxes[box]:
                    if label == label_in_box[0]:
                        #print(f"label {label} in box {box}")
                        label_in_box[1] = focal_length
                        break
                else:
                    boxes[box].append([label, focal_length])
                #print(f"+{boxes}")
        elif box in boxes and operation == '-':
            boxes[box] = [[val, key] for (val, key) in boxes[box] if val != label]
            #print(f"-{boxes}")
    print(f"{boxes}")

    # To confirm that all of the lenses are installed correctly, add up the focusing power of all of the lenses.
    sum_of_focusing_power = 0
    for box in boxes:
        for slot,lens in enumerate(boxes[box],1):
            #print(f"box: {box} lens: {lens[0]} slot: {slot} focal_length: {lens[1]}")
            focusing_power = (1 + box) * (slot) * (int(lens[1]))
            #print(f"box: {box} lens: {lens[0]} slot: {slot} focal_length: {lens[1]} focusing_power: {focusing_power}")
            sum_of_focusing_power += int(focusing_power)
    print(f"sum_of_focusing_power: {sum_of_focusing_power}")
    return sum_of_focusing_power

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
