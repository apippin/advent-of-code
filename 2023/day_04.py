from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re

# What day and year is this solution for?
day = 4
year = 2023

# Sample game data:
# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
raw = aoc_helper.fetch(day, year)

def parse_raw(raw: str):
    lines = raw.splitlines()
    data = list()
    for card, line in enumerate(lines,1):
        line = re.sub('Card\s+\d+: ','', line)
        cards = line.split(' | ')
        cards[0] = re.findall(r'\d+', cards[0])
        cards[1] = re.findall(r'\d+', cards[1])
        data.append(cards)
    return data

# Parse the game data
data = parse_raw(raw)

# In the above example, card 1 has five winning numbers (41, 48, 83, 86, and 17) and eight numbers
# you have (83, 86, 6, 31, 17, 9, 48, and 53). Of the numbers you have, four of them (48, 83, 17, and 86)
# are winning numbers! That means card 1 is worth 8 points (1 for the first match, then doubled three
# times for each of the three matches after the first).
# Take a seat in the large pile of colorful cards. How many points are they worth in total?
def part_one(data=data):
    #print(data)
    sum_of_points = 0
    for card_num, card in enumerate(data,1):
        points = 0
        winning_numbers = card[0]
        our_numbers = card[1]
        point_numbers = list()
        for num in our_numbers:
            if num in winning_numbers:
                point_numbers.append(num)
                if points == 0:
                    points = 1
                else:
                    points *= 2
        #print(f"winning_numbers: {winning_numbers} our_numbers: {our_numbers} point_numbers: {point_numbers} points: {points}")
        sum_of_points += points
    print(f"sum_of_points: {sum_of_points}")
    return sum_of_points

# Process all of the original and copied scratchcards until no more scratchcards are won.
# Including the original set of scratchcards, how many total scratchcards do you end up with?
def process_card(data, card_num, cards_won, card_matches):
    cards_won[card_num] += 1
    winning_numbers = data[card_num][0]
    our_numbers = data[card_num][1]
    matched_numbers = list()
    for num in our_numbers:
        if num in winning_numbers:
            matched_numbers.append(num)
    card_matches[card_num] = len(matched_numbers)
    #print(f"{card_num}: winning_numbers: {winning_numbers} our_numbers: {our_numbers} matched_numbers: {matched_numbers} num_matches: {num_matches}")

def part_two(data=data):
    cards_won = [0 for i in range(len(data))]
    card_matches = [0 for i in range(len(data))]
    for card_num, card in enumerate(data):
        process_card(data, card_num, cards_won, card_matches)
    for card_num, card in enumerate(cards_won):
        for x in range(card_num+1, card_num+card_matches[card_num]+1):
            cards_won[x] += cards_won[card_num]
    print(f"num_cards_won: {sum(cards_won)}")
    return sum(cards_won)

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
