#!/usr/bin/env python3
"""
AdventOfCode day 8.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
import functools


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


def check_end_locations(locations):
    """Check that all locations end with Z."""
    count = 0
    for location in locations:
        if location[2] != 'Z':
            break
        else:
            count += 1
    
    return count


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

    result = 0

    sequence = lines[0].strip('\n')

    nodes = {}
    for i in range(2, len(lines)):
        name = lines[i][0:3]
        left = lines[i][7:10]
        right = lines[i][12:15]
        nodes[name] = {'left': left, 'right': right}

    print(nodes)

    result = 0
    if args.second:
        # Find all XXA locations:
        locations = []
        for node in nodes.keys():
            if node[2] == 'A':
                locations.append(node)
        print(locations)

        result = 0
        loc_steps = []
        # Find XXZ pattern for each location
        for i in range(0, len(locations)):
            sequence_pos = 0
            location = locations[i]
            steps = 0
            while (location[2] != 'Z'):
                if sequence[sequence_pos] == 'L':
                    location = nodes[location]['left']
                else:
                    location = nodes[location]['right']
                steps += 1
                sequence_pos += 1
                if sequence_pos == len(sequence):
                    sequence_pos = 0
            loc_steps.append(steps)
            print(f"steps: {steps}, location: {location}")

        loc_steps.sort()
        found = False
        start_steps = loc_steps.pop()
        print(start_steps)
        steps = start_steps
        while not found:
            found = True
            for step in loc_steps:
                if steps % step != 0:
                    found = False
                    break
            steps += start_steps

        result = steps - start_steps

        #while not found:
        #    for i in range(0, len(locations)):
        #        if sequence[sequence_pos] == 'L':
        #            locations[i] = nodes[locations[i]]['left']
        #        else:
        #            locations[i] = nodes[locations[i]]['right']
        #    result += 1
        #    sequence_pos += 1
        #    if sequence_pos == len(sequence):
        #        sequence_pos = 0
        #    n = check_end_locations(locations)
        #    if n == len(locations):
        #        found = True
        #    elif n > 1:
        #        print(locations)

    else:
        location = 'AAA'
        sequence_pos = 0
        while (location != 'ZZZ'):
            if sequence[sequence_pos] == 'L':
                location = nodes[location]['left']
            else:
                location = nodes[location]['right']
            result += 1
            sequence_pos += 1
            if sequence_pos == len(sequence):
                sequence_pos = 0
            print(location)

    print(f"result: {result}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
