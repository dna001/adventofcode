#!/usr/bin/env python3
"""
AdventOfCode day 20.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
from pprint import pprint


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


def main():
    """Main program."""
    args = get_args()

    camera_tiles = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            tile_id = 0
            for line in file:
                line = line.strip('\n\r')
                if len(line) > 0 and 'Tile' in line:
                    tile_id = int(line.split(' ')[1][:-1])
                    tile = []
                    camera_tiles.append({'id': tile_id, 'array': tile})
                elif len(line) > 0:
                    row = []
                    for char in line:
                        if char == '#':
                            row.append(1)
                        else:
                            row.append(0)
                    tile.append(row)

    except IOError:
        print("Failed reading file!")
        sys.exit()

    #pprint(camera_tiles)

    # Calculate possible values for each tile
    for tile in camera_tiles:
        values = []
        # Left
        val = 0
        for row in tile['array']:
            val  = val << 1
            val += row[0]
        values.append(val)
        # Left inverted
        val = 0
        for pos in range(0, len(tile['array'])):
            val  = val << 1
            val += tile['array'][-(pos + 1)][0]
        values.append(val)
        # Right
        val = 0
        for row in tile['array']:
            val  = val << 1
            val += row[-1]
        values.append(val)
        # Right inverted
        val = 0
        for pos in range(0, len(tile['array'])):
            val  = val << 1
            val += tile['array'][-(pos + 1)][-1]
        values.append(val)
        # Top
        val = 0
        for col in tile['array'][0]:
            val  = val << 1
            val += col
        values.append(val)
        # Top inverted
        val = 0
        for pos in range(0, len(tile['array'])):
            val  = val << 1
            val += tile['array'][0][-(pos + 1)]
        values.append(val)
        # Bottom
        val = 0
        for col in tile['array'][-1]:
            val  = val << 1
            val += col
        values.append(val)
        # Bottom inverted
        val = 0
        for pos in range(0, len(tile['array'])):
            val  = val << 1
            val += tile['array'][-1][-(pos + 1)]
        values.append(val)
        tile['values'] = values

    #pprint(camera_tiles)

    # Find matches
    for pos_check in range(0, len(camera_tiles)):
        tile_check = camera_tiles[pos_check]
        tile_check['matches'] = []
        for pos in range(0, len(camera_tiles)):
            tile = camera_tiles[pos]
            match_found = False
            if tile_check == tile:
                continue
            for tile_check_val in tile_check['values']:
                for tile_val in tile['values']:
                    if tile_check_val == tile_val:
                        tile_check['matches'].append(tile['id'])
                        match_found = True
                        break
                if match_found:
                    break

    pprint(camera_tiles)

    answer = 1
    # Find corner tiles
    for tile in camera_tiles:
        if len(tile['matches']) == 2:
            answer *= tile['id']
            print(tile['id'])

    print("Answer: {}".format(answer))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
