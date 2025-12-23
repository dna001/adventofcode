#!/usr/bin/env python3
"""
AdventOfCode day 5.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
import math


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


def main():
    """Main program."""
    args = get_args()
    cargo_slots = [[], [], [], [], [], [], [], [], []]

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                if 'move' not in line:
                    # First x lines are cargo layout
                    if '[' in line:
                        for n in range(0, len(line)):
                            if line[n] == '[':
                                cargo_slots[math.floor(n / 4)].append(line[n + 1])
                elif 'move' in line:
                    print(f"Cargo slots: {cargo_slots}")
                    # Move stuff
                    split_line = line.split(' ')
                    no_moves = int(split_line[1])
                    from_slot = int(split_line[3])
                    to_slot = int(split_line[5])
                    print(f"move {no_moves} from {from_slot} to {to_slot}")
                    if args.second:
                        stack = cargo_slots[from_slot - 1][0: no_moves]
                        print(f"Stack: {stack}")
                        for move in range(0, no_moves):
                            cargo_slots[to_slot - 1].insert(0, stack[no_moves - move - 1])
                            # Remove all
                            cargo_slots[from_slot - 1].pop(0)
                    else:
                        for move in range(0, no_moves):
                            # Remove top from slot
                            item = cargo_slots[from_slot - 1].pop(0)
                            cargo_slots[to_slot - 1].insert(0, item)

                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    #for cargo_slot in cargo_slots:
    #    cargo_slot.reverse()

    print(f"Cargo slots: {cargo_slots}")

    answer = ""
    for cargo_slot in cargo_slots:
        if len(cargo_slot) > 0:
            answer += cargo_slot[0]

    print(f"Answer: {answer}")

    #print(f"Rucksacks: {rucksacks}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
