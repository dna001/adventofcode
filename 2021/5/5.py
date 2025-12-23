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
    lines = []

    min_x = sys.maxsize
    max_x = 0
    min_y = sys.maxsize
    max_y = 0

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                coords = line.strip('\n\r').split(' -> ')
                start = coords[0].split(',')
                end = coords[1].split(',')
                if int(start[0]) < min_x:
                    min_x = int(start[0])
                if int(start[0]) > max_x:
                    max_x = int(start[0])
                if int(end[0]) < min_x:
                    min_x = int(end[0])
                if int(end[0]) > max_x:
                    max_x = int(end[0])
                if int(start[1]) < min_y:
                    min_y = int(start[1])
                if int(start[1]) > max_y:
                    max_y = int(start[1])
                if int(end[1]) < min_y:
                    min_y = int(end[1])
                if int(end[1]) > max_y:
                    max_y = int(end[1])

                l = {'x0': int(start[0]), 'y0': int(start[1]),
                     'x1': int(end[0]), 'y1': int(end[1])}
                lines.append(l)
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(lines)
    print(f"min/max x {min_x}/{max_x}, min/max y {min_y}/{max_y}")

    map = [[0] * (max_x + 1) for _ in range(max_y + 1)]
    for line in lines:
        # Just check horizontal/vertical lines
        if line['x0'] == line['x1']:
            if line['y0'] < line['y1']:
                start = line['y0']
                end = line['y1']
            else:
                start = line['y1']
                end = line['y0']
            for y in range(start, end + 1):
                map[y][line['x0']] += 1

        elif line['y0'] == line['y1']:
            if line['x0'] < line['x1']:
                start = line['x0']
                end = line['x1']
            else:
                start = line['x1']
                end = line['x0']
            for x in range(start, end + 1):
                map[line['y0']][x] += 1
        elif args.second:
            #diagonal lines
            print(line)
            if line['x0'] < line['x1']:
                x_step = 1
            else:
                x_step = -1
            if line['y0'] < line['y1']:
                y_step = 1
            else:
                y_step = -1
            x = line['x0']
            y = line['y0']
            for _ in range(0, abs(line['x1'] - line['x0']) + 1):
                map[y][x] += 1
                x += x_step
                y += y_step

    for line in map:
        print(line)

    num_crossing_lines = 0
    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            if map[y][x] > 1:
                num_crossing_lines += 1

    print(f"Crossing lines {num_crossing_lines}")
    #answer = board_unmarked_sum * number
    #print(f"Answer {board_unmarked_sum} * {number} = {answer}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
