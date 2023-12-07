from collections import defaultdict, deque
from typing import TYPE_CHECKING
import aoc_helper

import re
import operator
from functools import reduce

# What day and year is this solution for?
day = 7
year = 2023

# Game globals
...

# Sample game data:
# 32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483
raw = aoc_helper.fetch(day, year)

def matching_cards(dict, search):
    return [card for card, num in dict.items() if num == search]

def hand_type(cards, part_two=False):
    # Calculate the type of the hand:
    # Five of a kind = 7
    # Four of a kind = 6
    # Full House = 5
    # Three of a kind = 4
    # Two pair = 3
    # One pair = 2
    # High card = 1
    if part_two and 'J' in cards:
        jokers = cards['J']
    else:
        jokers = 0
    #print(f"cards: {cards} jokers: {jokers}")
    if matching_cards(cards, 5-jokers) or jokers == 5:
        return 7
    elif matching_cards(cards, 4-jokers):
        return 6
    elif ((matching_cards(cards, 2-jokers) and matching_cards(cards,3)) or
          (matching_cards(cards, 2) and matching_cards(cards,3-jokers))):
        return 5
    elif matching_cards(cards, 3-jokers):
        return 4
    elif (len(matching_cards(cards, 2)) == 2) or ((len(matching_cards(cards, 2)) == 1) and jokers and matching_cards(cards, 1)):
        return 3
    elif (len(matching_cards(cards, 2)) == 1) or (jokers and matching_cards(cards, 1)):
        return 2
    elif matching_cards(cards, 1):
        return 1

def strength_of_cards(hand, part_two=False):
    strengths = list()
    for i,card in enumerate(hand):
        if card.isnumeric():
            strengths.append(int(card))
        else:
            match card:
                case 'T':
                    strengths.append(10)
                case 'J':
                    if not part_two:
                        strengths.append(11)
                    else:
                        strengths.append(1)
                case 'Q':
                    strengths.append(12)
                case 'K':
                    strengths.append(13)
                case 'A':
                    strengths.append(14)
    return strengths

def parse_raw(raw: str):
    part_two = True # Manually change to False for part_one, True for part_two
    lines = raw.splitlines()
    data = list()
    for line in lines:
        cards = dict()
        tokens = line.split(" ")
        hand = tokens[0]
        bid = int(tokens[1])
        for i, c in enumerate(hand):
            if c not in cards:
                cards[c] = 1
            else:
                cards[c] += 1
        data.append((hand, bid, hand_type(cards, part_two), strength_of_cards(hand, part_two)))
    return data

# Parse the game data
data = parse_raw(raw)

# Now, you can determine the total winnings of this set of hands by adding up the
# result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5).
# So the total winnings in this example are 6440.
# Find the rank of every hand in your set. What are the total winnings?
def part_one(data=data):
    #print(f"{data}")
    sorted_hands = sorted(data, key=lambda x: (x[2], (x[3][0], x[3][1], x[3][2], x[3][3], x[3][4])), reverse=True)
    print(f"{sorted_hands}")
    winnings = 0
    max_hands = len(sorted_hands)
    for i, hand in enumerate(sorted_hands):
        print(f"rank: {max_hands -i}")
        winnings += (max_hands - i) * hand[1]
    print(f"total winnings: {winnings}")
    return winnings

# Using the new joker rule, find the rank of every hand in your set.
# What are the new total winnings?
def part_two(data=data):
    winnings = part_one(data)
    return winnings

# Check that the test data then full data works for part_one
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)

# Check that the test data then full data works for part_two
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
