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

    # Read input
    try:
        with open(args.input, 'rt') as file:
            lines = file.readlines()
    except IOError:
        print("Failed reading file!")
        sys.exit()

    dial_value = 50
    rotation_list = []
    for line in lines:
        line = line.strip('\n')
        if line[0] == "R":
            rotation_list.append(int(line[1:]))
        else:
            rotation_list.append(-1*int(line[1:]))

    if args.second:
        password = 0
        for rotation in rotation_list:
            step = 1
            if rotation < 0:
                step = -1
                rotation = rotation * -1
            for x in range(rotation):
                dial_value += step
                if dial_value < 0:
                    dial_value = 99
                if dial_value > 99:
                    dial_value = 0
                if dial_value == 0:
                    password += 1

        print(f'Password {password}')
    else:
        password = 0
        for rotation in rotation_list:
            dial_value += rotation
            if dial_value > 99:
                dial_value = dial_value % 100
            if dial_value < 0:
                while dial_value < 0:
                    dial_value += 100
            if dial_value == 0:
                password += 1

        print(f'Password {password}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
