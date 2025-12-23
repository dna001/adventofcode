#!/usr/bin/env python3
"""
AdventOfCode day 11.
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


def print_map(map):
    """Print map."""
    for row in map:
        row_string = ""
        for col in row:
            row_string += str(col)
        print(row_string)


def execute_rule(stone):
    """Execute rule on stone and return list of new number(s)."""
    new_stones = []
    digit_string = str(stone)
    if stone  == 0:
        new_stones.append(1)
    elif len(digit_string) % 2 == 0:
        # Even number of digits
        left_number = int(digit_string[0: len(digit_string) // 2])
        right_number = int(digit_string[len(digit_string) // 2:])
        new_stones.append(left_number)
        new_stones.append(right_number)
    else:
        new_stones.append(stone * 2024)
    
    return new_stones


def execute_rule_recursive(stone, iterations, total_stones):
    """Execute rule on stone and return list of new number(s)."""
    if iterations == 0:
        total_stones['total'] += 1
        #print(f"{stone}")
        return

    new_stones = []
    digit_string = str(stone)
    if stone  == 0:
        new_stones.append(1)
    elif len(digit_string) % 2 == 0:
        # Even number of digits
        left_number = int(digit_string[0: len(digit_string) // 2])
        right_number = int(digit_string[len(digit_string) // 2:])
        new_stones.append(left_number)
        new_stones.append(right_number)
    else:
        new_stones.append(stone * 2024)
    
    if iterations > 0:
        for new_stone in new_stones:
            execute_rule_recursive(new_stone, iterations - 1, total_stones)


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

    stone_list = []
    for line in lines:
        line = line.strip('\n')
        values = line.split(' ')
        for value in values:
            stone_list.append(int(value))

    print(stone_list)

    if args.second:
        blinks = 30
        total_stones = {'total' : 0}
        for stone in stone_list:
            execute_rule_recursive(stone, blinks, total_stones)
            print(f"Stone {stone} complete")

        print(f"Number of stones after {blinks} blinks: {total_stones['total']}")
    else:
        blinks = 25
        for i in range(blinks):
            new_stone_list = []
            for stone in stone_list:
                new_stone_list += execute_rule(stone)
            print(f"iteration {i}, {len(new_stone_list)}")
            print(new_stone_list)
            stone_list = new_stone_list

        print(f"Number of stones after {blinks} blinks: {len(stone_list)}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
