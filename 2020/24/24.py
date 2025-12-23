#!/usr/bin/env python3
"""
AdventOfCode day 24.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
from pprint import pprint
from enum import Enum


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


def parse_tile_instructions(line):
    """Parse tile instructions"""
    pos = 0
    x = 0
    y = 0
    # e, se, sw, w, nw, and ne
    #print(line)
    while pos < len(line):
        direction = line[pos : pos + 2]
        #print(direction)
        if direction == 'se':
            x += 1
            y -= 1
            pos += 2
        elif direction == 'sw':
            y -= 1
            pos += 2
        elif direction == 'nw':
            x -= 1
            y += 1
            pos += 2
        elif direction == 'ne':
            y += 1
            pos += 2
        elif direction[0] == 'e':
            x += 1
            pos += 1
        elif direction[0] == 'w':
            x -= 1
            pos += 1

    return {'x': x, 'y': y}


def main():
    """Main program."""
    args = get_args()

    black_tiles = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            for line in file:
                line = line.strip('\n\r')
                coords = parse_tile_instructions(line)
                print(coords)
                found = False
                for tile in black_tiles:
                    if coords['x'] == tile['x'] and coords['y'] == tile['y']:
                        black_tiles.remove(tile)
                        found = True
                        print("Found!")
                        break
                if not found:
                    black_tiles.append(coords)

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(black_tiles)

    print("Number of black tiles: {}".format(len(black_tiles)))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
