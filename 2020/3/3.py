#!/usr/bin/env python3
"""
AdventOfCode day 3.
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


def validate_password(line):
    """Validate password."""
    split = line.split(' ')
    min_times = int(split[0].split('-')[0])
    max_times = int(split[0].split('-')[1])
    char = split[1].strip(':')
    password = split[2]
    # Count char in password
    count = 0
    for ch in password:
        if ch == char:
            count += 1

    if count >= min_times and count <= max_times:
        return True
    else:
        print("{}-{} {}: {}".format(min_times, max_times, char, password))
        return False


def main():
    """Main program."""
    args = get_args()
    lines = []
    x = 0
    y = 0
    x_steps = [1,3,5,7,1]
    y_steps = [1,1,1,1,2]
    n_trees = 0
    total_trees = [0,0,0,0,0]
    result = 1

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline().strip('\n')
            while line:
                lines.append(line)
                line = file.readline()
    except IOError:
        print("Failed reading file!")
        sys.exit()


    for count in range(0, len(x_steps)):
        n_trees = 0
        x = 0
        y = 0
        while y < len(lines):
            if lines[y][x] == '#':
                n_trees += 1
            x = (x + x_steps[count]) % len(lines[0])
            y += y_steps[count]

        total_trees[count] = n_trees
        print("Number of trees: {} ({}/{})".format(n_trees, x_steps[count], y_steps[count]))

    for trees in total_trees:
        result *= trees

    print("Multiply result: {}".format(result))        
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
