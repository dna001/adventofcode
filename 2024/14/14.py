#!/usr/bin/env python3
"""
AdventOfCode day 14.
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
            if col == 0:
                row_string += '.'
            else:
                row_string += 'x' # str(col)
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

    robots = []
    for line in lines:
        values = line.strip('\n').split(' ')
        x_and_y = values[0].split(',')
        p_x = int(x_and_y[0][2:])
        p_y = int(x_and_y[1])
        x_and_y = values[1].split(',')
        v_x = int(x_and_y[0][2:])
        v_y = int(x_and_y[1])
        robot_vector = {'p': {'x': p_x, 'y': p_y}, 'v': {'x': v_x, 'y': v_y}}
        robots.append(robot_vector)

    print(robots)

    if args.input.find('test') > 0:
        width = 11
        height = 7
    else:
        width = 101
        height = 103

    map = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(0)
        map.append(row)

    print_map(map)

    if args.second:
        for s in range(10000):
            for robot in robots:
                robot['p']['x'] += robot['v']['x']
                robot['p']['y'] += robot['v']['y']
                if robot['p']['x'] < 0:
                    robot['p']['x'] += width
                elif robot['p']['x'] >= width:
                    robot['p']['x'] -= width
                if robot['p']['y'] < 0:
                    robot['p']['y'] += height
                elif robot['p']['y'] >= height:
                    robot['p']['y'] -= height

            # print on map
            if (s - 108) % width == 0:
                print(f"S: {s}")
                map = []
                for y in range(height):
                    row = []
                    for x in range(width):
                        row.append(0)
                    map.append(row)
                for robot in robots:
                    x = robot['p']['x']
                    y = robot['p']['y']
                    map[y][x] += 1

                print_map(map)

    else:
        for s in range(100):
            for robot in robots:
                robot['p']['x'] += robot['v']['x']
                robot['p']['y'] += robot['v']['y']
                if robot['p']['x'] < 0:
                    robot['p']['x'] += width
                elif robot['p']['x'] >= width:
                    robot['p']['x'] -= width
                if robot['p']['y'] < 0:
                    robot['p']['y'] += height
                elif robot['p']['y'] >= height:
                    robot['p']['y'] -= height

        # print on map and count each quadrant
        print()
        quad = {'ul': 0, 'ur': 0, 'bl': 0, 'br': 0}
        for robot in robots:
            x = robot['p']['x']
            y = robot['p']['y']
            map[y][x] += 1
            # Upper left
            if x < width // 2 and y < height // 2:
                quad['ul'] += 1
            elif x > width // 2 and y < height // 2:
                quad['ur'] += 1
            elif x < width // 2 and y > height // 2:
                quad['bl'] += 1
            elif x > width // 2 and y > height // 2:
                quad['br'] += 1

        print_map(map)
        print(quad)
        safety_factor = quad['ul'] * quad['ur'] * quad['bl'] * quad['br']
        print(f"Safety factor: {safety_factor}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
