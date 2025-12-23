#!/usr/bin/env python3
"""
AdventOfCode day 8.
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

    map = []
    for line in lines:
        line = line.strip('\n')
        col_array = []
        for char in line:
            col_array.append(char)
        map.append(col_array)

    map_antinodes = []
    for row in map:
        new_row = []
        for x in range(len(row)):
            new_row.append(row[x])
        map_antinodes.append(new_row)

    print_map(map, map_antinodes)

    antenna_freqs = {}
    # Find antennas
    for y in range(len(map)):
        for x in range(len(map[0])):
            antenna = map[y][x]
            pos = {'x': x, 'y': y}
            if antenna != '.':
                if antenna in antenna_freqs:
                    antenna_freqs[antenna].append(pos)
                else:
                    antenna_freqs[antenna] = [pos]

    print(antenna_freqs)

    if args.second:
        # Find antinodes (resonant harmonics)
        for antenna_key in antenna_freqs:
            antennas = antenna_freqs[antenna_key]
            print(antennas)
            # Check all combos of 2 antennas
            for i in range(len(antennas) - 1):
                for j in range(i + 1, len(antennas)):
                    dist_x = antennas[i]['x'] - antennas[j]['x']
                    dist_y = antennas[i]['y'] - antennas[j]['y']
                    antinode_1_x = antennas[j]['x'] + dist_x
                    antinode_1_y = antennas[j]['y'] + dist_y
                    while antinode_1_x >= 0 and antinode_1_x < len(map[0]) and \
                       antinode_1_y >=0 and antinode_1_y < len(map):
                        map_antinodes[antinode_1_y][antinode_1_x] = '#'
                        antinode_1_x += dist_x
                        antinode_1_y += dist_y
                    antinode_2_x = antennas[i]['x'] - dist_x
                    antinode_2_y = antennas[i]['y'] - dist_y
                    while antinode_2_x >= 0 and antinode_2_x < len(map[0]) and \
                       antinode_2_y >=0 and antinode_2_y < len(map):
                        map_antinodes[antinode_2_y][antinode_2_x] = '#'
                        antinode_2_x -= dist_x
                        antinode_2_y -= dist_y
                    # print(f"dist: {dist_x}, {dist_y}, an1 {antinode_1_x}, {antinode_1_y}")

        print_map(map, map_antinodes)
        antinode_count = 0
        # Count unique antinodes
        for row in map_antinodes:
            for col in row:
                if col == '#':
                    antinode_count += 1
        # Add antennas (> 1)
        #for antenna_key in antenna_freqs:
        #    if len(antenna_freqs[antenna_key]) > 1:
        #        antinode_count += 1

        print(f"Unique antinode count: {antinode_count}")
    else:
        # Find antinodes
        for antenna_key in antenna_freqs:
            antennas = antenna_freqs[antenna_key]
            print(antennas)

            # Check all combos of 2 antennas
            for i in range(len(antennas) - 1):
                for j in range(i + 1, len(antennas)):
                    dist_x = antennas[i]['x'] - antennas[j]['x']
                    dist_y = antennas[i]['y'] - antennas[j]['y']
                    antinode_1_x = antennas[i]['x'] + dist_x
                    antinode_1_y = antennas[i]['y'] + dist_y
                    antinode_2_x = antennas[j]['x'] - dist_x
                    antinode_2_y = antennas[j]['y'] - dist_y
                    print(f"dist: {dist_x}, {dist_y}, an1 {antinode_1_x}, {antinode_1_y}")
                    if antinode_1_x >= 0 and antinode_1_x < len(map[0]) and \
                       antinode_1_y >=0 and antinode_1_y < len(map):
                        map_antinodes[antinode_1_y][antinode_1_x] = '#'
                    if antinode_2_x >= 0 and antinode_2_x < len(map[0]) and \
                       antinode_2_y >=0 and antinode_2_y < len(map):
                        map_antinodes[antinode_2_y][antinode_2_x] = '#'

        print_map(map, map_antinodes)
        antinode_count = 0
        # Count unique antinodes
        for row in map_antinodes:
            for col in row:
                if col == '#':
                    antinode_count += 1

        print(f"Unique antinode count: {antinode_count}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
