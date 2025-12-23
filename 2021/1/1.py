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
    values = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                values.append(int(line))
                line = file.readline()
    except IOError:
        print("Failed reading file!")
        sys.exit()

    increases = 0
    if not args.second:
        old_value = values[0]
        for n in range(1, len(values)):
            if old_value < values[n]:
                increases += 1
            old_value = values[n]
    else:
        # Sliding window of 3 values
        old_window = values[0] + values[1] + values[2]
        print(f"Old window {old_window}")
        for n in range(3, len(values)):
            new_window = values[n - 2] + values[n - 1] + values[n]
            print(f"New window {new_window}")
            if old_window < new_window:
                increases += 1
            old_window = new_window

    print(f"Increases {increases}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
