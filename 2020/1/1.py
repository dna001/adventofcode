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

    for n in range(0,len(values)):
        for m in range(n + 1,len(values)):
            if not args.second:
                if values[n] + values[m] == 2020:
                    print("{} * {} = {}".format(values[n], values[m], values[n] * values[m]))
                    exit()
            else:
                for l in range(m + 1,len(values)):
                    if values[n] + values[m] + values[l] == 2020:
                        print("{} * {} * {} = {}".format(values[n], values[m], values[l],
                            values[n] * values[m] * values[l]))
                        exit()

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
