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


def main():
    """Main program."""
    args = get_args()
    directions = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                cmd, value = line.split(' ')
                directions.append((cmd, int(value)))
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    if not args.second:
        depth = 0
        forward = 0
        for item in directions:
            if item[0] == 'forward':
                forward += item[1]
            elif item[0] == 'down':
                depth += item[1]
            elif item[0] == 'up':
                depth -= item[1]

        print(f"Forward {forward}, Depth {depth}")
        answer = depth * forward
        print(f"Answer {depth} * {forward} = {answer}")

    else:
        depth = 0
        forward = 0
        aim = 0
        for item in directions:
            if item[0] == 'forward':
                forward += item[1]
                depth += item[1] * aim
            elif item[0] == 'down':
                aim += item[1]
            elif item[0] == 'up':
                aim -= item[1]

        print(f"Forward {forward}, Depth {depth}, Aim {aim}")
        answer = depth * forward
        print(f"Answer {depth} * {forward} = {answer}")


    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
