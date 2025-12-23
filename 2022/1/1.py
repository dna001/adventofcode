#!/usr/bin/env python3
"""
AdventOfCode day 1.
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
    no_of_elfs = 0
    elves = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            lines = file.readlines()
            calories = 0
            for line in lines:
                line = line.strip('\n')
                if len(line) > 0:
                    calories += int(line)
                else:
                    elves.append(calories)
                    calories = 0
    except IOError:
        print("Failed reading file!")
        sys.exit()

    elves.sort()

    print(f"Elves {elves}")

    if args.second:
        print(f"Most calories (3 top elves) {elves[-1] + elves[-2] + elves[-3]}")
    else:
        print(f"Most calories {elves[-1]}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
