#!/usr/bin/env python3
"""
AdventOfCode day 10.
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


def test_adapters(adapters):
    """Test adapters."""
    jolt = 0
    old_adapter = 0
    ones = 0
    threes = 0

    adapters.append(adapters[len(adapters) - 1] + 3)

    for adapter in adapters:
        if adapter - old_adapter == 1:
            ones += 1
        elif adapter - old_adapter == 3:
            threes += 1
        old_adapter = adapter

    return (ones, threes)


def main():
    """Main program."""
    args = get_args()
    total_adapters = 0
    adapters = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                line = line.strip('\n\r')
                adapters.append(int(line))
                total_adapters += 1
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    adapters.sort()

    print(adapters)

    one, three = test_adapters(adapters)

    print("1 jolt diff: {}, 3 jolt diff: {}, total: {}, answer: {}".format(one, three, total_adapters,
        one * three))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
