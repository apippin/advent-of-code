from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
import sys

# What day and year is this solution for?
day = 5
year = 2023

# maps: seed-to-soil, soil-to-fertilizer, fertilizer-to-water, water-to-light,
# light-to-temperature, temperature-to-humidity, humidity-to-location
raw = aoc_helper.fetch(day, year)

# Parse out the seeds and maps and store them in our global data dictionary
def get_map(lines, data, line_num, name):
    line_num += 1
    data[name] = list()
    while line_num < len(lines) and lines[line_num].strip():
        data[name].append(tuple(map(int, re.findall(r"(\d+)", lines[line_num]))))
        line_num += 1

def parse_raw(raw: str):
    lines = raw.splitlines()
    line_num = 0
    data = dict()
    while line_num < len(lines):
        if "seeds" in lines[line_num]:
            data["seeds"] = tuple(map(int, re.findall(r"(\d+)", lines[line_num])))
        elif "map" in lines[line_num]:
            name = lines[line_num].split(' ')
            get_map(lines, data, line_num, name[0])
        line_num += 1
    return data

# Parse the game data
data = parse_raw(raw)

# What is the lowest location number that corresponds to any of the initial seed numbers?
# data mapping: index 0=destination range start 1=source range start 2=range length
def get_dest(data, name, src):
    for m in data[name]:
        if(src >= m[1] and src < m[1] + m[2]):
            dst = m[0] + (src - m[1])
            #print(f"src:{src} dst:{dst}")
            return dst
    return src

def get_location(data, seed):
    soil = get_dest(data, "seed-to-soil", seed)
    fertilizer = get_dest(data, "soil-to-fertilizer", soil)
    water = get_dest(data, "fertilizer-to-water", fertilizer)
    light = get_dest(data, "water-to-light", water)
    temperature = get_dest(data, "light-to-temperature", light)
    humidity = get_dest(data, "temperature-to-humidity", temperature)
    location = get_dest(data, "humidity-to-location", humidity)
    return location

def part_one(data=data):
    min_location = sys.maxsize
    # Get the locations of each seed
    for seed in data["seeds"]:
        location = get_location(data, seed)
        if location < min_location:
            min_location = location
    print(f"min location: {min_location}")
    return min_location

# Consider all of the initial seed numbers listed in the ranges on the first line of the almanac.
# What is the lowest location number that corresponds to any of the initial seed numbers?
def get_src(data, name, dst):
    for m in data[name]:
        if(dst >= m[0] and dst < m[0] + m[2]):
            src = m[1] + (dst - m[0])
            #print(f"src:{src} dst:{dst}")
            return src
    return dst

def get_seed(data, location):
    humidity = get_src(data, "humidity-to-location", location)
    temperature = get_src(data, "temperature-to-humidity", humidity)
    light = get_src(data, "light-to-temperature", temperature)
    water = get_src(data, "water-to-light", light)
    fertilizer = get_src(data, "fertilizer-to-water", water)
    soil = get_src(data, "soil-to-fertilizer", fertilizer)
    seed = get_src(data, "seed-to-soil", soil)
    return seed

def valid_seed(data, seed):
    ranges = iter(data["seeds"])
    seed_ranges = [*zip(ranges, ranges)]
    #print(f"Seed ranges: {seed_ranges}")
    # For each seed in the range of seeds, get their locations
    for seed_range in seed_ranges:
        if seed >= seed_range[0] and seed < seed_range[0] + seed_range[1]:
            return True
    return False

def part_two(data=data):
    max_location = sys.maxsize
    # We can't use the approach from part1 because it would take 4-6 hours with this dataset.
    # So brute force would work using part1 solution, but would take too long.
    # Therefore, we have to use a different approach that would run faster.
    # Let's start at the lowest possible location until the highest location,
    # search backwards through the mapping from a location back to a seed.
    # Check if that seed is valid. If it is, by definition, we have our lowest location.
    # Since there are way fewer locations than seeds, this will run much faster.
    for location in range(0, max_location):
        seed = get_seed(data, location)
        if valid_seed(data, seed):
            # The first valid seed we find, by definition, will have the lowest location
            # as we are searching for locations from 0 ... MAXINT
            print(f"seed: {seed} location: {location}")
            break
    print(f"min location: {location}")
    return location

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
