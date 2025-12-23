#!/usr/bin/env python3
"""
AdventOfCode day 4.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime


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


def count_cards(cards, card):
    """ Count cards for card."""
    card_id = card['card_id']
    for id in range(card_id + 1, card_id + card['wins'] + 1):
        cards[id]['count'] += 1
        # Recursive
        count_cards(cards, cards[id])


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
    if args.second:
        cards = []
        card_id = 0
        for line in lines:
            card_parts = line.strip('\n').split(":")[1]
            card_parts = card_parts.split('|')
            winners = card_parts[0].split(' ')
            have = card_parts[1].split(' ')
            matches = []
            for w in winners:
                if w in have and w != '':
                    matches.append(w)
            print(matches)
            card = {'card_id': card_id, 'wins': len(matches), 'count': 1}
            cards.append(card)
            card_id += 1
        
        for card in cards:
            count_cards(cards, card)
        print(cards)
        for card in cards:
            result += card['count']
    else:
        for line in lines:
            card_parts = line.strip('\n').split(":")[1]
            card_parts = card_parts.split('|')
            winners = card_parts[0].split(' ')
            have = card_parts[1].split(' ')
            matches = []
            for w in winners:
                if w in have and w != '':
                    matches.append(w)
            print(matches)
            points = 0
            if len(matches) > 0:
                points = 1 << (len(matches) - 1)
            print(points)
            result += points

    print(f"result: {result}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
