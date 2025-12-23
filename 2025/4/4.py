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

def count_adjacent(grid, x, y):
    """ Count adjacent paper rolls. """
    count = 0
    for xx in range(-1, 2):
        for yy in range (-1, 2):
            xxx = x + xx
            yyy = y + yy
            if xx == 0 and yy == 0:
                continue
            if xxx >= 0 and xxx < len(grid[0]) and \
               yyy >= 0 and yyy < len(grid):
                if grid[yyy][xxx] == '@':
                    count += 1
    return count


def find_movable_paper_rolls(grid):
    """ Find removable paper rolls. """
    positions = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '@':
                count = count_adjacent(grid, x, y)
                if count < 4:
                    positions.append({'x':x, 'y':y, 'count': count})
    return positions


def remove_rolls_from_grid(grid, roll_list):
    """ Remove rolls from grid. """
    for roll in roll_list:
        grid[roll['y']][roll['x']] = '.'


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

    grid = []
    for line in lines:
        row = []
        line = line.strip('\n')
        for c in line:
            row.append(c)
        grid.append(row)

    if args.second:
        answer = 0
        last_count = 1
        while last_count > 0:
            rolls = find_movable_paper_rolls(grid)
            last_count = len(rolls)
            print(last_count)
            answer += len(rolls)
            remove_rolls_from_grid(grid, rolls)

        print(f'Answer {answer}')
    else:
        answer = find_movable_paper_rolls(grid)

        #print(answer)
        print(f'Answer {len(answer)}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
