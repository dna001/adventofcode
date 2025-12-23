#!/usr/bin/env python3
"""
AdventOfCode day 6.
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


def main():
    """Main program."""
    args = get_args()
    fish_list = [0] * 9

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            for fish in line.strip("\n\r").split(','):
                fish_list[int(fish)] += 1

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(fish_list)

    if not args.second:
        days = 80
    else:
        days = 256

    for day in range(0, days):
        new_fish = fish_list[0]
        for n in range(1, len(fish_list)):
            fish_list[n - 1] = fish_list[n]
        fish_list[8] = new_fish
        fish_list[6] += new_fish
        print(f"Day {day}: {fish_list}, new fish {new_fish}")

    # Fish summary
    answer = 0
    for fish in fish_list:
        answer += fish

    print(f"Answer: after {days} days, {answer}")

    #answer = board_unmarked_sum * number
    #print(f"Answer {board_unmarked_sum} * {number} = {answer}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
