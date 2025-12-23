#!/usr/bin/env python3
"""
AdventOfCode day 9.
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

    rows = []
    min_pos = sys.maxsize
    max_pos = 0

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                cols = []
                for c in line.strip("\n\r"):
                    cols.append(int(c))
                rows.append(cols)
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(rows)

    risk_level = 0
    for y in range(0, len(rows)):
        for x in range(0, len(rows[0])):
            # Check adjacent for lowest point
            value = rows[y][x]
            if x > 0:
                left = rows[y][x - 1]
            else:
                left = 10
            if x < len(rows[0]) - 1:
                right = rows[y][x + 1]
            else:
                right = 10
            if y > 0:
                up = rows[y - 1][x]
            else:
                up = 10
            if y < len(rows) - 1:
                down = rows[y + 1][x]
            else:
                down = 10
            if value < left and value < right and value < up and value < down:
                risk_level += value + 1

    print(f"Answer: {risk_level}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
