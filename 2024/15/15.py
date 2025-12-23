#!/usr/bin/env python3
"""
AdventOfCode day 15.
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
            row_string += col
        print(row_string)


def move_boxes(map, boxes, x_dir, y_dir):
    """Move all boxes one step in dir."""
    #print(boxes)
    boxes.reverse()
    #print(boxes)
    for box in boxes:
        map[box['y'] + y_dir][box['x'] + x_dir] = 'O'

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
    map_done = False
    moves = ""
    for line in lines:
        line = line.strip('\n')
        if len(line) == 0:
            map_done = True
            continue
        if not map_done:
            row = []
            for char in line:
                row.append(char)
            map.append(row)
        else:
            moves += line

    print_map(map)
    print(moves)

    # Find start position:
    start_pos = {'x': 0, 'y': 0}
    found = False
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == '@':
                start_pos['x'] = x
                start_pos['y'] = y
                #map[y][x] = '.'
                found = True
                break
        if found:
            break

    print(start_pos)

    if args.second:
        print(f"")
    else:
        pos = start_pos
        # Move robot
        for move in moves:
            boxes = []
            x = pos['x']
            y = pos['y']
            if move == '^':
                for y in range(pos['y'] - 1, 0, -1):
                    if map[y][x] == '.':
                        # Move boxes
                        if len(boxes) > 0:
                            move_boxes(map, boxes, 0, -1)
                        map[pos['y']][pos['x']] = '.'
                        pos['y'] -= 1
                        map[pos['y']][pos['x']] = '@'
                        break
                    elif map[y][x] == 'O':
                        boxes.append({'x':x, 'y': y})
                    elif map[y][x] == '#':
                        break
            elif move == '>':
                for x in range(pos['x'] + 1, len(map[0])):
                    if map[y][x] == '.':
                        # Move boxes
                        if len(boxes) > 0:
                            move_boxes(map, boxes, 1, 0)
                        map[pos['y']][pos['x']] = '.'
                        pos['x'] += 1
                        map[pos['y']][pos['x']] = '@'
                        break
                    elif map[y][x] == 'O':
                        boxes.append({'x':x, 'y': y})
                    elif map[y][x] == '#':
                        break
            elif move == 'v':
                for y in range(pos['y'] + 1, len(map)):
                    if map[y][x] == '.':
                        # Move boxes
                        if len(boxes) > 0:
                            move_boxes(map, boxes, 0, 1)
                        map[pos['y']][pos['x']] = '.'
                        pos['y'] += 1
                        map[pos['y']][pos['x']] = '@'
                        break
                    elif map[y][x] == 'O':
                        boxes.append({'x': x, 'y': y})
                    elif map[y][x] == '#':
                        break
            elif move == '<':
                for x in range(pos['x'] - 1, 0, -1):
                    if map[y][x] == '.':
                        # Move boxes
                        if len(boxes) > 0:
                            move_boxes(map, boxes, -1, 0)
                        map[pos['y']][pos['x']] = '.'
                        pos['x'] -= 1
                        map[pos['y']][pos['x']] = '@'
                        break
                    elif map[y][x] == 'O':
                        boxes.append({'x':x, 'y': y})
                    elif map[y][x] == '#':
                        break
            print(f"Move: {move} to {pos}")
            #print_map(map)
        # Calculate GPS coord sum
        gps_sum = 0
        for y in range(len(map)):
            for x in range(len(map[0])):
                if map[y][x] == 'O':
                    gps = 100 * y + x
                    gps_sum += gps
        print_map(map)
        print(f"GPS sum: {gps_sum}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
