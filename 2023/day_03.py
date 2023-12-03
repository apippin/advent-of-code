from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

#import re
#import operator
#from functools import reduce
import numpy as np

# What day and year is this solution for?
day = 3
year = 2023

# Game globals
syms = '"!@#$%^&*()-+?_=,<>/"'

# Sample game data:
# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
raw = aoc_helper.fetch(day, year)

# Parse each row (string) into a list of characters to give us a 2 dimensional array
def parse_raw(raw: str):
    lines = raw.splitlines()
    data= []
    for line in lines:
        data.append([*line])
    return data

# Parse the game data
data = parse_raw(raw)

# In this schematic, two numbers are not part numbers because they are not adjacent to a symbol:
# 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.
# Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
def prev_row(data, row: int):
    if 0 <= row-1 < len(data):
        return row-1
    return 0

def next_row(data, row: int):
    if 0 <= row+1 < len(data):
        return row+1
    return row

def prev_col(data, col: int):
    if 0 <= col-1 < len(data[0]):
        return col-1
    return 0

def next_col(data, col: int):
    if 0 <= col+1 < len(data[0]):
        return col+1
    return col

def part_one(data=data):
    sum_of_part_numbers = 0
    for row,line in enumerate(data):
        part_num = ""
        found_part_num = False
        for col,char in enumerate(line):
            if char.isnumeric():
                part_num += char
                # Check if this number is adjacent to a symbol
                if (data[row][prev_col(data, col)] in syms or # left
                    data[row][next_col(data, col)] in syms or # right
                    data[prev_row(data, row)][col] in syms or # up
                    data[next_row(data, row)][col] in syms or # down
                    data[prev_row(data, row)][prev_col(data, col)] in syms or # diagonal up left
                    data[prev_row(data, row)][next_col(data, col)] in syms or # diagonal up right
                    data[next_row(data, row)][prev_col(data, col)] in syms or # diagonal down left
                    data[next_row(data, row)][next_col(data, col)] in syms): # diagonal down right
                    # This number is part of a valid part number
                    #print(f"data[{row}][{col}] = {char}")
                    found_part_num = True
            else:
                if found_part_num:
                    #print(f"data[{row}][{col}] = {int(part_num)}")
                    sum_of_part_numbers += int(part_num)
                found_part_num = False
                part_num = ""
        if found_part_num:
            #print(f"data[{row}][{col}] = {int(part_num)}")
            sum_of_part_numbers += int(part_num)
            found_part_num = False
            part_num = ""

    print(f"sum_of_part_numbers: {sum_of_part_numbers}")
    return sum_of_part_numbers

# This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.
# In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345.
# The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.)
# Adding up all of the gear ratios produces 467835.
# What is the sum of all of the gear ratios in your engine schematic?

def find_part_num(data, gear, num, row, col, left=True, right=True):
    # Go left
    if left:
        for x in range(col,-1,-1):
            if data[row][x].isnumeric():
                gear[num] = data[row][x] + gear[num]
            else:
                break
    # Go right
    if right:
        for x in range(col+1,len(data[row]),1):
            if data[row][x].isnumeric():
                gear[num] += data[row][x]
            else:
                break

def part_two(data=data):
    sum_of_gear_ratios = 0
    for row,line in enumerate(data):
        for col,char in enumerate(line):
            if char == '*':
                # Check if this '*' is adjacent to 2 part numbers

                # Create an array that can hold up to 8 gears, initalize each gear position to ''
                gear = np.full(8, '', dtype='object')

                # diagonal up left
                if data[prev_row(data, row)][prev_col(data, col)].isnumeric():
                    find_part_num(data, gear, 0, prev_row(data, row), prev_col(data, col))

                # diagonal up right
                if data[prev_row(data, row)][next_col(data, col)].isnumeric():
                    find_part_num(data, gear, 1, prev_row(data, row), next_col(data, col))

                # up
                if data[prev_row(data, row)][col].isnumeric():
                    find_part_num(data, gear, 2, prev_row(data, row), col)

                # You can't have the same number in all 3 positions
                if gear[0] == gear[1] == gear[2]:
                    gear[1] = ''
                    gear[2] = ''
                # You can't have the same number in down if you have either diagonal
                elif gear[0] == gear[2] or gear[1] == gear[2]:
                    gear[2] = ''

                # diagonal down left
                if data[next_row(data, row)][prev_col(data, col)].isnumeric():
                    find_part_num(data, gear, 3, next_row(data, row), prev_col(data, col))

                # diagonal down right
                if data[next_row(data, row)][next_col(data, col)].isnumeric():
                    find_part_num(data, gear, 4, next_row(data, row), next_col(data, col))

                # down
                if data[next_row(data, row)][col].isnumeric():
                    find_part_num(data, gear, 5, next_row(data, row), col)

                # You can't have the same number in all 3 positions
                if gear[3] == gear[4] == gear[5]:
                    gear[4] = ''
                    gear[5] = ''
                # You can't have the same number in down if you have either diagonal
                elif gear[3] == gear[5] or gear[4] == gear[5]:
                    gear[5] = ''

                # left
                if data[row][prev_col(data, col)].isnumeric():
                    find_part_num(data, gear, 6, row, col-1, True, False)

                # right
                if data[row][next_col(data, col)].isnumeric():
                    find_part_num(data, gear, 7, row, col, False, True)

                # If you found 2 gears, create a gear ratio and add it to our sum of them
                #print(f"gears: {gear}")
                # Convert our list of strings into a list of ints, converting null values to 0
                gear_int = np.array([int(i) if i else 0 for i in gear], dtype=int)
                # If we have 2 gears, multiply them together to get a gear ratio and add to the final answer
                if np.count_nonzero(gear_int) == 2:
                    # Multiply all non-zero gears together
                    gear_ratio = np.prod(gear_int[gear_int != 0])
                    sum_of_gear_ratios += gear_ratio
                    #print(f"row {row} found gears {gear_int} gear_ratio: {gear_ratio}")

    print(f"sum_of_gear_ratios: {sum_of_gear_ratios}")
    return sum_of_gear_ratios


# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
