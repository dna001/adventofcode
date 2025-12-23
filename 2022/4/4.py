#!/usr/bin/env python3
"""
AdventOfCode day 4.
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


def find_overlap(elf_pair):
    """Find complete overlaps."""
    if elf_pair['start1'] >= elf_pair['start2'] and elf_pair['stop1'] <= elf_pair['stop2']:
        # pair 2 inside of pair 1
        return 1
    elif elf_pair['start2'] >= elf_pair['start1'] and elf_pair['stop2'] <= elf_pair['stop1']:
        # pair 1 inside of pair 2
        return 1

    return 0


def find_all_overlap(elf_pair):
    """Find all overlaps."""
    for section in range(elf_pair['start1'], elf_pair['stop1'] + 1):
        if section in range(elf_pair['start2'], elf_pair['stop2'] + 1):
            return 1
    return 0


def main():
    """Main program."""
    args = get_args()
    elf_pairs = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                elfs = line.strip('\n').split(',')
                elf_pair = {'start1': int(elfs[0].split('-')[0]), 'stop1': int(elfs[0].split('-')[1]),
                            'start2': int(elfs[1].split('-')[0]), 'stop2': int(elfs[1].split('-')[1])}
                print(f"Elf pair: {elf_pair}")
                elf_pairs.append(elf_pair)
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    #print(f"Rucksacks: {rucksacks}")

    overlap_sum = 0

    if args.second:
        for elf_pair in elf_pairs:
            overlap_sum += find_all_overlap(elf_pair)
        print(f"Partial overlaps: {overlap_sum}")
    else:
        for elf_pair in elf_pairs:
            overlap_sum += find_overlap(elf_pair)
        print(f"Complete overlaps: {overlap_sum}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
