#!/usr/bin/env python3
"""
AdventOfCode day 9.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
import math
import copy

sum_of_total_sizes = 0

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


def check_adjacent(pos1, pos2):
    """ Check if positions are adjacent or same. """
    for y in range(pos1['y'] - 1, pos1['y'] + 2):
        for x in range(pos1['x'] - 1, pos1['x'] + 2):
            if pos2['x'] == x and pos2['y'] == y:
                return True
    return False


def add_new_pos(path, pos):
    """ Add new positions if not existing. """
    for p in path:
        #print(p)
        if p['x'] == pos['x'] and p['y'] == pos['y']:
            #print("skip")
            return
    path.append(pos)


def main():
    """Main program."""
    args = get_args()
    dir_table = {'L': {'x': -1, 'y': 0},
                 'R': {'x': 1, 'y': 0},
                 'U': {'x': 0, 'y': -1},
                 'D': {'x': 0, 'y': 1}}
    tail_path = [{'x': 0, 'y': 0}]
    tail_pos = {'x': 0, 'y': 0}
    head_pos = {'x': 0, 'y': 0}

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline().strip('\n')
            while line:
                line_split = line.split(' ')
                direction = line_split[0]
                count = line_split[1]
                for _ in range(0, int(count)):
                    # Move head
                    head_pos['x'] += dir_table[direction]['x']
                    head_pos['y'] += dir_table[direction]['y']
                    # Move tail
                    if not check_adjacent(tail_pos, head_pos):
                        if tail_pos['x'] != head_pos['x'] and tail_pos['y'] != head_pos['y']:
                            # Move diagonally
                            if direction == 'L':
                                tail_pos['x'] = head_pos['x'] + 1
                                tail_pos['y'] = head_pos['y']
                            elif direction == 'R':
                                tail_pos['x'] = head_pos['x'] - 1
                                tail_pos['y'] = head_pos['y']
                            elif direction == 'U':
                                tail_pos['x'] = head_pos['x']
                                tail_pos['y'] = head_pos['y'] + 1
                            elif direction == 'D':
                                tail_pos['x'] = head_pos['x']
                                tail_pos['y'] = head_pos['y'] - 1
                        else:
                            # Follow
                            tail_pos['x'] += dir_table[direction]['x']
                            tail_pos['y'] += dir_table[direction]['y']
                    add_new_pos(tail_path, copy.copy(tail_pos))
                    print(f"Head: {head_pos}, Tail: {tail_pos}")
                line = file.readline().strip('\n')

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(tail_path)
    print(f"Unique positions: {len(tail_path)}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
