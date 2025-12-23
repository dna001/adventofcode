#!/usr/bin/env python3
"""
AdventOfCode day 21.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime


class Dice:
    def __init__(self):
        self.rolls = 0
        self.value = 1

    def roll(self):
        """Roll dice and return value."""
        val = self.value
        self.value += 1
        if self.value > 1000:
            self.value = 1
        self.rolls += 1
        return val


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


def main():
    """Main program."""
    args = get_args()

    players = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                start_pos = int(line.strip("\n\r").split(':')[1])
                players.append({'pos': start_pos, 'score': 0})
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(players)

    dice = Dice()
    if not args.second:
        current_player = 0
        while players[0]['score'] < 1000 and players[1]['score'] < 1000:
            # Roll 3x deterministic dice
            dice_sum = 0
            for _ in range(3):
                dice_sum += dice.roll()
            pos = players[current_player]['pos']
            pos += dice_sum
            pos = ((pos - 1) % 10) + 1
            players[current_player]['pos'] = pos
            players[current_player]['score'] += pos
            current_player = (current_player + 1) % 2
            #print(f"After step {step}: {len(polymer_template)}")

    score = players[current_player]['score']
    print(f"Answer: {score} * {dice.rolls} = {score * dice.rolls}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
