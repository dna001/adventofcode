#!/usr/bin/env python3
"""
AdventOfCode day 10.
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


def find_next_trail_step(target_height, x, y, map, trail_index, trail_count_list):
    """Find next higher trail step."""
    if x < 0 or x >= len(map[0]) or y < 0 or y >= len(map):
        return
    if map[y][x] == target_height:
        #print(f"{target_height}, {x}, {y}")
        if target_height == 9:
            key = str(y * len(map) + x)
            if key in trail_count_list[trail_index]:
                trail_count_list[trail_index][key] += 1
            else: 
                trail_count_list[trail_index][key] = 1
            print(f"Found trail end for {trail_index} at {x},{y}")
        else:
            # Right
            find_next_trail_step(target_height + 1, x + 1, y, map, trail_index, trail_count_list)
            # Down
            find_next_trail_step(target_height + 1, x, y + 1, map, trail_index, trail_count_list)
            # Left
            find_next_trail_step(target_height + 1, x - 1, y, map, trail_index, trail_count_list)
            # Up
            find_next_trail_step(target_height + 1, x, y - 1, map, trail_index, trail_count_list)


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

    map = []
    for line in lines:
        line = line.strip('\n')
        col = []
        for char in line:
            col.append(int(char))
        map.append(col)

    print_map(map)

    trail_count_list = []
    trail_id = 0
    # Find trails
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == 0:
                trail_count_list.append({})
                find_next_trail_step(0, x, y, map, trail_id, trail_count_list)
                trail_id += 1

    if args.second:
        trail_score_sum = 0
        for trails in trail_count_list:
            trail_score = 0
            for _, value in trails.items():
                trail_score += value
            print(f"Trail score: {trail_score}")
            trail_score_sum += trail_score

        print(f"Trail score sum {trail_score_sum}")
    else:
        trail_score_sum = 0
        for trail in trail_count_list:
            print(f"Trail score: {len(trail)}")
            trail_score_sum += len(trail)

        print(f"Trail score sum {trail_score_sum}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
