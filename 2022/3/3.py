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


def get_priority(ch):
    """Get priority of item."""
    if ch >= 'a' and ch <= 'z':
        priority = ord(ch) - ord('a') + 1
    else:
        priority = ord(ch) - ord('A') + 27

    return priority


def find_common_item(r1, r2, r3):
    """Find common item in rucksacks."""
    for ch1 in r1:
        start_r2 = 0
        for r2_offset in range(start_r2, len(r2)):
            if ch1 == r2[r2_offset]:
                for ch3 in r3:
                    if ch1 == ch3:
                        return ch1

    return 'bla'


def main():
    """Main program."""
    args = get_args()
    rucksacks = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                rucksacks.append(line.strip('\n'))
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    #print(f"Rucksacks: {rucksacks}")

    total_priority = 0

    if args.second:
        for group in range(0, len(rucksacks), 3):
            r1 = rucksacks[group]
            r2 = rucksacks[group + 1]
            r3 = rucksacks[group + 2]
            common_item = find_common_item(r1, r2, r3)
            if len(common_item) != 1:
                print("Error!!")
                exit(0)
            print(f"Multiple occurence: {common_item}")
            total_priority += get_priority(common_item)
    else:
        for rucksack in rucksacks:
            first_half = rucksack[0:int(len(rucksack)/2)]
            second_half = rucksack[int(len(rucksack)/2):]
            # Find first multiple occurences
            found = False
            for ch in first_half:
                start = 0
                for offset in range(start, len(second_half)):
                    if ch == second_half[offset]:
                        total_priority += get_priority(ch)
                        print(f"Multiple occurence: {ch}")
                        found = True
                        break
                if found:
                    break
                start += 1

    print(f"Total priority: {total_priority}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
