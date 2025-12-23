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
    crab_positions = []

    min_pos = sys.maxsize
    max_pos = 0

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            for crab in line.strip("\n\r").split(','):
                crab_positions.append(int(crab))
                min_pos = min(int(crab), min_pos)
                max_pos = max(int(crab), max_pos)

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(crab_positions)
    print(f"min: {min_pos}, max {max_pos}")

    # Brute force position finder
    min_cost = sys.maxsize
    for pos in range(min_pos, max_pos + 1):
        # Calculate cost
        cost = 0
        for crab in crab_positions:
            if not args.second:
                cost += abs(crab - pos)
            else:
                steps = abs(crab - pos)
                cost += int((steps * (steps + 1)) / 2)
        if cost < min_cost:
            min_cost = cost
            best_pos = pos

    print(f"Best position: {best_pos}, cost: {min_cost}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
