#!/usr/bin/env python3
"""
AdventOfCode day 19.
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


def myFunc(e):
  """Sort based on string length."""
  return len(e)


def find_matching_towel(pattern, towels, found):
    """Find towel matching pattern."""
    for towel in towels:
        if pattern[0: len(towel)] == towel:
            if len(pattern) == len(towel):
                found['found'] = True
                print(f"Found at towel {towel}")
                break
            else:
                find_matching_towel(pattern[len(towel):], towels, found)
                if found['found']:
                    break


def find_towels(patterns, towels, possible_designs):
    """Find towels matching patterns."""
    for pattern in patterns:
        pos = 0
        
        retest_towels = []
        retest = False
        found = {'found': False}
        find_matching_towel(pattern, towels, found)

        if found['found']:
            print(f"{pattern} match found")
            if pattern not in possible_designs:
                possible_designs.append(pattern)
        else:
            print(f"{pattern} match not found")
  

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

    towels = []
    patterns = []
    towels_done = False
    for line in lines:
        line = line.strip('\n')
        if len(line) == 0:
            towels_done = True
            continue
        if not towels_done:
            values = line.split(', ')
            for value in values:
                towels.append(value)
        else:
            patterns.append(line)

    print(towels)
    print(patterns)

    # Sort towels
    towels.sort(reverse=True, key=myFunc)
    print(towels)

    if args.second:
        print(f"")
    else:
        possible_designs = []
        find_towels(patterns, towels, possible_designs)

        print(f"Possible designs: {len(possible_designs)}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
