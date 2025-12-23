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


def print_map(map, map_antinodes):
    """Print map."""
    for row in range(len(map)):
        row_string = ""
        for col in range(len(map[0])):
            if map_antinodes[row][col] == '.':
                row_string += map[row][col]
            else:
                row_string += map_antinodes[row][col]
        print(row_string)


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

    disk_map = []
    for line in lines:
        line = line.strip('\n')
        for char in line:
            disk_map.append(int(char))

    print(disk_map)

    # Extended disk map
    disk_map_ext = []
    file = True
    id = 0
    for value in disk_map:
        if file:
            for i in range(value):
                disk_map_ext.append(str(id))
            id += 1
            file = False
        else:
            for i in range(value):
                disk_map_ext.append('.')
            file = True
    
    print(disk_map_ext)

    if args.second:
        print(f"")
    else:
        # Defrag
        pos_from_end = 1
        for i in range(len(disk_map_ext)):
            if i >= len(disk_map_ext):
                break
            if disk_map_ext[i] == '.':
                last_pos = disk_map_ext.pop()
                while (last_pos == '.'):
                    last_pos = disk_map_ext.pop()
                    if i + 1 >= len(disk_map_ext):
                        break
                disk_map_ext[i] = last_pos

        print(disk_map_ext)
        # Calculate checksum
        checksum = 0
        for i in range(len(disk_map_ext)):
            if disk_map_ext[i] != '.':
                checksum += i * int(disk_map_ext[i])

        print(f"Checksum: {checksum}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
