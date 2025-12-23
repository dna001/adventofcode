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


def check_valid(rows, x, y):
    """Check for adjacent symbols."""
    valid = False
    if (x > 0):
        if rows[y][x - 1] in "0123456789":
            pass
        elif rows[y][x - 1] != '.':
            valid = True
    if (x < len(rows[0]) - 1):
        if rows[y][x + 1] in "0123456789":
            pass
        elif rows[y][x + 1] != '.':
            valid = True
    if (y > 0) and (x > 0):
        if rows[y - 1][x - 1] != '.':
            valid = True
    if (y > 0):
        if rows[y - 1][x] != '.':
            valid = True
    if (y > 0) and (x < len(rows[0]) - 1):
        if rows[y - 1][x + 1] != '.':
            valid = True
    if (y < len(rows) - 1) and x > 0:
        if rows[y + 1][x - 1] != '.':
            valid = True
    if (y < len(rows) - 1):
        if rows[y + 1][x] != '.':
            valid = True
    if (y < len(rows) - 1) and (x < len(rows[0]) - 1):
        if rows[y + 1][x + 1] != '.':
            valid = True
    return valid


def get_gear_value(x, y, id_grid, lookup):
    """Get gear value."""
    value = 0
    part_list = []
    for y1 in range(max(0, y - 1), min(len(id_grid), y + 2)):
        for x1 in range(max(0, x - 1), min(len(id_grid[0]), x + 2)):
            #print(f"x1: {x1} y1: {y1}")
            if x1 == x and y1 == y:
                pass
            else:
                id = id_grid[y1][x1]
                if id >= 0:
                    if id not in part_list:
                        part_list.append(id)
    if len(part_list) == 2:
        value = lookup[part_list[0]] * lookup[part_list[1]]
    print(f"val: {value}, part_count: {len(part_list)}")
    return value


def main():
    """Main program."""
    args = get_args()
    cal_value_sum = 0

    # Read input
    try:
        with open(args.input, 'rt') as file:
            lines = file.readlines()
    except IOError:
        print("Failed reading file!")
        sys.exit()

    result = 0
    rows = []
    for line in lines:
        line = line.strip('\n')
        rows.append(line)

    if args.second:
        lookup = {}
        id_grid = []
        id = 0
        for y in range(0, len(rows)):
            grid_row = []
            row = rows[y]
            number = 0
            for x in range(0, len(row)):
                c = row[x]
                if c in "0123456789":
                    number *= 10
                    number += int(c)
                    grid_row.append(id)
                else:
                    if number > 0:
                        print(number)
                        lookup[id] = number
                        id += 1
                    number = 0
                    grid_row.append(-1)
            if number > 0:
                print(number)
                lookup[id] = number
                id += 1
            id_grid.append(grid_row)

        for y in range(0, len(rows)):
            row = rows[y]
            for x in range(0, len(row)):
                if row[x] == '*':
                    value = get_gear_value(x, y, id_grid, lookup)
                    result += value

    else:
        for y in range(0, len(rows)):
            row = rows[y]
            number = 0
            valid = False
            for x in range(0, len(row)):
                c = row[x]
                if c in "0123456789":
                    number *= 10
                    number += int(c)
                    # Check all sides
                    if check_valid(rows, x, y):
                        valid = True
                else:
                    if valid:
                        print(number)
                        result += number
                    number = 0
                    valid = False
            if valid:
                print(number)
                result += number

    print(f"result: {result}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
