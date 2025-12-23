#!/usr/bin/env python3
"""
AdventOfCode day 13.
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


def find_point(list, point):
    """Find point in list."""
    for p in list:
        if p['x'] == point['x'] and p['y'] == point['y']:
            return True

    return False


def fold(points, axis, axis_value):
    """Fold paper along specified axis and return resulting points"""
    new_points = []

    for point in points:
        x = point['x']
        y = point['y']
        if axis == 'x' and x > axis_value:
            x = axis_value - (x - axis_value)
            new_point = {'x': x, 'y': y}
            if not find_point(points, new_point):
                new_points.append(new_point)
        elif axis == 'y' and y > axis_value:
            y = axis_value - (y - axis_value)
            new_point = {'x': x, 'y': y}
            if not find_point(points, new_point):
                new_points.append(new_point)
        else:
            new_point = {'x': x, 'y': y}
            new_points.append(new_point)

    return new_points


def main():
    """Main program."""
    args = get_args()

    paper_coordinates = []
    fold_instructions = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                line = line.strip("\n\r")
                if line.find('fold along x') >= 0:
                    val = int(line.split('=')[1])
                    fold_instructions.append({'axis': 'x', 'value': val})
                elif line.find('fold along y') >= 0:
                    val = int(line.split('=')[1])
                    fold_instructions.append({'axis': 'y', 'value': val})
                elif line.find(',') >= 0:
                    coords = line.split(',')
                    paper_coordinates.append({'x': int(coords[0]), 'y': int(coords[1])})
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(paper_coordinates)
    print(fold_instructions)

    if not args.second:
        # Fold instruction 1
        points = fold(paper_coordinates, fold_instructions[0]['axis'], fold_instructions[0]['value'])

        print(points)

        print(f"Answer: {len(points)}")
    else:
        # Fold all instructions
        for instruction in fold_instructions:
            new_points = fold(paper_coordinates, instruction['axis'], instruction['value'])
            paper_coordinates = new_points

        print(f"Dots = {len(paper_coordinates)}")
        max_x = 0
        max_y = 0
        #Find max x and y
        for point in paper_coordinates:
            if point['x'] > max_x:
                max_x = point['x']
            if point['y'] > max_y:
                max_y = point['y']

        # Draw
        for y in range(max_y + 1):
            line = ""
            for x in range(max_x + 1):
                if find_point(paper_coordinates, {'x': x, 'y': y}):
                    line += '#'
                else:
                    line += '.'
            print(line)

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
