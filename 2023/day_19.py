from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
from math import prod

# What day and year is this solution for?
day = 19
year = 2023

# Game globals
...

# Sample game data:
"""
x: Extremely cool looking
m: Musical (it makes a noise when you hit it)
a: Aerodynamic
s: Shiny

px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
raw = aoc_helper.fetch(day, year)

# Read all the workflows in and store them in a dictionary of lists
# Read all the parts in and store them in a list of dictionaries
def parse_raw(raw: str):
    lines = raw.splitlines()
    read_parts = False
    data = {"parts": [], "workflows": {}}
    for line in lines:
        if line == "":
            read_parts = True
            continue
        if read_parts:
            parts = line[:-1][1:].split(',')
            data["parts"].append({p.split('=')[0]:int(p.split('=')[1]) for p in parts})
        else:
            key = line.split('{')[0]
            flow = line.split('{')[1][:-1].split(',')
            data["workflows"][key] = flow
    return data

# Parse the game data
data = parse_raw(raw)

# Check if we are in a terminal state (accepted or rejected)
def terminal_state(data, accepted_parts, part, next):
    if next in 'AR':
        if next in 'A':
            accepted_parts.append(part)
        return True
    return False

# Parse a flow in a a workflow into its different pieces
def parse_flow(flow):
    rating = None
    operator = None
    value =  None
    next = None
    match = re.search("(\w)([<>])(\d+):(\w+)", flow)
    if match:
        rating = match[1]
        operator = match[2]
        value = int(match[3])
        next = match[4]
    else:
        match = re.search("(\w+)$", flow)
        if match:
            next = match[1]
    return rating, operator, value, next

# Sort through all of the parts you've been given;
# what do you get if you add together all of the rating
# numbers for all of the parts that ultimately get accepted?
def part_one(data=data):
    #print(data["workflows"])
    #print(*data["parts"],sep="\n")
    accepted_parts = []
    for part in data["parts"]:
        done = False
        workflow = data["workflows"]["in"]
        #print(f"checking part: {part}")
        while not done:
            for flow in workflow:
                rating, operator, value, next = parse_flow(flow)
                #print(f"checking flow: rating: {rating} operator: {operator} value: {value} next: {next}")
                if not rating and next:
                    #print(f"=> {next}")
                    done = terminal_state(data, accepted_parts, part, next)
                    if not done:
                        workflow = data["workflows"][next]
                    break
                elif rating and operator and value and next:
                    #print(f"{rating} {operator} {value} => {next}")
                    match operator:
                        case '>':
                            #print(f"checking rating: {part[rating]} > value: {value}")
                            if part[rating] > value:
                                #print(f"=> {next}")
                                done = terminal_state(data, accepted_parts, part, next)
                                if not done:
                                    workflow = data["workflows"][next]
                                break
                        case '<':
                            #print(f"checking rating: {part[rating]} < value: {value}")
                            if part[rating] < value:
                                #print(f"=> {next}")
                                done = terminal_state(data, accepted_parts, part, next)
                                if not done:
                                    workflow = data["workflows"][next]
                                break
                else:
                    print(f"#ERROR: Unsupported workflow: {flow}")
    #print(*accepted_parts, sep="\n")
    sum_of_ratings = 0
    for part in accepted_parts:
        sum_of_ratings += sum(part.values())
    print(f"sum_of_ratings: {sum_of_ratings}")
    return sum_of_ratings

# Consider only your list of workflows; the list of part ratings that the Elves wanted you to sort is no longer relevant.
# How many distinct combinations of ratings will be accepted by the Elves' workflows?
def part_two(data=data):
    # Follow the workflows.
    # Each workflow reduces one of the 'x', 'm', 'a', 's' range.
    # If we end up in an accepted state, store these reduced ranges in the solution vector.
    todo = [{"state": "in", "x": (1,4000), "m": (1,4000), "a": (1,4000), "s": (1,4000)}]

    total = 0
    while todo:
        cur = todo.pop()
        state = cur["state"]

        if state == "R":
            continue
        elif state == "A":
            # For each such tuple take the product of the lengths of these ranges, and sum them up.
            total += prod(cur[d][1]-cur[d][0]+1 for d in "xmas")
        else:
            for flow in data["workflows"][state]:
                rating, operator, value, next = parse_flow(flow)
                split = dict(cur)
                split["state"] = next
                if operator == "<":
                    split[rating] = (split[rating][0], value-1)
                    cur[rating] = (value, cur[rating][1])
                elif operator == ">":
                    split[rating] = (value+1, split[rating][1])
                    cur[rating] = (cur[rating][0], value)
                todo.append(split)
    print(f"distinct_combinations: {total}")
    return total

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
