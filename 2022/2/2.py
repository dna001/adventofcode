#!/usr/bin/env python3
"""
AdventOfCode day 2.
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


def calc_result(elf, me):
    """Calculate result of rock/paper/scissors."""
    points = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}
    my_score = points[me]

    if points[elf] == points[me] - 1 or (points[elf] == 3 and points[me] == 1):
        # win
        my_score += 6
    elif points[elf] == points[me]:
        # draw
        my_score += 3

    print(f"{elf} vs {me} score: {my_score}")
    return my_score


def get_proper_value(elf, rule):
    """Get proper value for me."""
    lose = {'A': 'Z', 'B': 'X', 'C': 'Y'}
    draw = {'A': 'X', 'B': 'Y', 'C': 'Z'}
    win = {'A': 'Y', 'B': 'Z', 'C': 'X'}
    if rule == 'X':
        # lose
        me = lose[elf]
    elif rule == 'Y':
        # draw
        me = draw[elf]
    else:
        # win
        me = win[elf]

    return me


def main():
    """Main program."""
    args = get_args()
    total_score = 0

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                values = line.strip('\n').split(" ")
                elf = values[0]
                me = values[1]
                if args.second:
                    me = get_proper_value(elf, me)
                total_score += calc_result(elf, me)
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(f"My score {total_score}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
