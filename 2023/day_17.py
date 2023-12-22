from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
import heapq

# What day and year is this solution for?
day = 17
year = 2023

# Globals
# (x,y) = Up, Right, Down, Left
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Sample game data:
"""
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""
raw = aoc_helper.fetch(day, year)

# Read each number into its own (x,y) map with its value being the number
def parse_raw(raw: str):
    lines = raw.splitlines()
    data = [[int(y) for y in x] for x in lines]
    return data

# Parse the game data
data = parse_raw(raw)

def find_lowest_heat_path(data, min_dist, max_dist):
    # What is our final destination coordinates
    dest_y = len(data) - 1
    dest_x = len(data[0]) - 1
    # We will use heap commands to push and pop stuff off this queue
    # The items will be tuples, with the first element being the cost
    # The priority queue will keep items sorted by the lowest cost
    # Popping an item off this queue will always give us the next node to visit
    # since you always need to visit the next lowest cost node next
    # Queue of unvisited nodes (heat, x, y, sd=skipDirection)
    unvisited = [(0, 0, 0, -1)]
    # Set of visited nodes
    visited = set()
    # Key = (x, y, direction) Value = heat_loss
    heat_losses = {}
    # While we still have nodes to visit in our queue
    while unvisited:
        heat_loss, x, y, skipDir = heapq.heappop(unvisited)
        #print(f"visiting: ({x},{y}) l={heat_loss} skipD={skipDir}")
        # If we have reached our final destination return the heat_loss for this node
        if x == dest_x and y == dest_y:
            return heat_loss
        # If we have already visited this node, skip it
        if (x, y, skipDir) in visited:
            continue
        visited.add((x, y, skipDir))
        for direction in range(len(DIRS)):
            heat_loss_inc = 0
            # Check to make sure we can go this direction
            # We can't go this direction if:
            # 1) The direction is one we should skip because we already visited this node from this direction
            # 2) The direction would take us backwards
            if direction == skipDir or (direction + 2) % 4 == skipDir:
                continue
            # We need to check each node going in this direction up until our maximum direction node count
            for distance in range(1, max_dist + 1):
                new_x = x + DIRS[direction][0] * distance
                new_y = y + DIRS[direction][1] * distance
                # Check to make sure our new locations are still in the bounds of our data grid
                if new_y in range(len(data)) and new_x in range(len(data[0])):
                    # What would our heat loss increase by going to this node?
                    heat_loss_inc += data[new_y][new_x]
                    # If our distance is less than the minimum distance, we can go no further
                    if distance < min_dist:
                        continue
                    # Update what our new heat loss would be for going to this node
                    new_heat_loss = heat_loss + heat_loss_inc
                    if heat_losses.get((new_x, new_y, direction), 1e1000) <= new_heat_loss:
                        continue
                    heat_losses[(new_x, new_y, direction)] = new_heat_loss
                    heapq.heappush(unvisited, (new_heat_loss, new_x, new_y, direction))
        #print(f"unvisited: {unvisited}")
        #print(f"heat_losses: {heat_losses}")

# Directing the crucible from the lava pool to the machine parts factory,
# but not moving more than three consecutive blocks in the same direction,
# what is the least heat loss it can incur?
def part_one(data=data):
    # We'll need to use Dijkstra’s algorithm to find the path that minimizes heat loss
    # Minimum distance in one direction is 1, maximum distance in one direction is 3
    #print(*data, sep='\n')
    heat_loss = find_lowest_heat_path(data, 1, 3)
    print(f"heat_loss: {heat_loss}")
    return heat_loss

# Once an ultra crucible starts moving in a direction,
# it needs to move a minimum of four blocks in that direction before it can turn (or even before it can stop at the end).
# However, it will eventually start to get wobbly: an ultra crucible can move a maximum of ten consecutive blocks without turning.
# Directing the ultra crucible from the lava pool to the machine parts factory,
# what is the least heat loss it can incur?
def part_two(data=data):
    #print(*data, sep='\n')
    heat_loss = find_lowest_heat_path(data, 4, 10)
    print(f"heat_loss: {heat_loss}")
    return heat_loss

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
