#!/usr/bin/env python3
"""
AdventOfCode day 7.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
import functools


def get_args():
    """Parse args from terminal."""
    parser = argparse.ArgumentParser(
        description='AdventOfCode')
    parser.add_argument(
        '-i',
        '--input',
        help='Input file',
        required=True)

    parser.add_argument(
        '-s',
        '--second',
        help='Input file',
        action='store_true',
        default=False)

    return parser.parse_args()


def find_type(hand):
    """Find type of hand."""
    bin = {}
    type = 0
    for card in hand:
        if card in bin.keys():
            bin[card] += 1
        else:
            bin[card] = 1

    for card in bin.keys():
        diff_count = 0
        if bin[card] == 5:
            # Five of a kind
            type = 7
            break
        elif bin[card] == 4:
            # Four of a kind
            type = 6
            break
        elif bin[card] == 3:
            if type == 2:
                # Full house
                type = 5
                break
            else:
                # Three of a kind
                type = 4
        elif bin[card] == 2:
            if type == 2:
                # Two pair
                type = 3
                break
            elif type == 4:
                # Full house
                type = 5
                break
            else:
                # One pair
                type = 2
        elif bin[card] == 1:
            diff_count += 1
            if diff_count == 5:
                type = 1
                break
    return type


def compare(x, y):
    """Compare function for suite."""
    converter = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4,'7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
    diff = x['type'] - y['type']
    if diff == 0:
        # Find highest card
        for i in range(0, 5):
            a = converter[x['hand'][i]]
            b = converter[y['hand'][i]]
            if a != b:
                return a - b
        assert(False)
    else:
        return diff


def find_type_joker(hand):
    """Find type of hand with joker rule."""
    bin = {}
    type = 0
    for card in hand:
        if card in bin.keys():
            bin[card] += 1
        else:
            bin[card] = 1

    joker_count = 0
    if 'J' in bin.keys():
        joker_count = bin['J']
        bin.pop('J')

    if joker_count == 5:
        return 7

    # Sort by value
    bin = dict(sorted(bin.items(), key=lambda item: item[1], reverse=True))
    print(bin)

    for card in bin.keys():
        diff_count = 0
        print(f"{card}, {bin[card]}")
        if bin[card] == 5:
            # Five of a kind
            type = 7
            break
        elif bin[card] + joker_count == 5:
            # Five of a kind
            joker_count = 0
            type = 7
            break
        elif bin[card] == 4:
            # Four of a kind
            type = 6
            break
        elif bin[card] + joker_count == 4:
            # Four of a kind
            joker_count = 0
            type = 6
            break
        elif bin[card] == 3:
            if type == 2:
                # Full house
                type = 5
                break
            else:
                # Three of a kind
                type = 4
        elif bin[card] + joker_count == 3:
            joker_count = 0
            if type == 2:
                # Full house
                type = 5
                break
            else:
                # Three of a kind
                type = 4
        elif bin[card] == 2:
            if type == 2:
                # Two pair
                type = 3
                break
            elif type == 4:
                # Full house
                type = 5
                break
            else:
                # One pair
                type = 2
        elif bin[card] + joker_count == 2:
            joker_count = 0
            if type == 2:
                # Two pair
                type = 3
                break
            elif type == 4:
                # Full house
                type = 5
                break
            else:
                # One pair
                type = 2
        elif bin[card] == 1:
            diff_count += 1
            if diff_count == 5:
                type = 1
                break
    return type


def compare_joker(x, y):
    """Compare function for suite with joker weakest."""
    converter = {'J': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5,'7': 6, '8': 7, '9': 8, 'T': 9, 'Q': 10, 'K': 11, 'A': 12}
    diff = x['type'] - y['type']
    if diff == 0:
        # Find highest card
        for i in range(0, 5):
            a = converter[x['hand'][i]]
            b = converter[y['hand'][i]]
            if a != b:
                return a - b
        assert(False)
    else:
        return diff


def main():
    """Main program."""
    args = get_args()

    # Read input
    try:
        with open(args.input, 'rt') as file:
            lines = file.readlines()
    except IOError:
        print("Failed reading file!")
        sys.exit()

    result = 0
    hands = []
    for line in lines:
        hand = {'hand': line.split(' ')[0], 'bid': int(line.strip('\n').split(' ')[1])}
        hands.append(hand)
    #print(hands)

    if args.second:
        # Find type of hand
        for hand in hands:
            hand['type'] = find_type_joker(hand['hand'])

        print(hands)

        sorted_list = sorted(hands, key=functools.cmp_to_key(compare_joker))
        print(sorted_list)
        print(len(sorted_list))
    else:
        # Find type of hand
        for hand in hands:
            hand['type'] = find_type(hand['hand'])

        #print(hands)

        sorted_list = sorted(hands, key=functools.cmp_to_key(compare))
        print(sorted_list)
        print(len(sorted_list))

    multiplier = 1
    for hand in sorted_list:
        result += multiplier * hand['bid']
        multiplier += 1

    print(f"result: {result}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
