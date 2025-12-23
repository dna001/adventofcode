#!/usr/bin/env python3
"""
AdventOfCode day 12.
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


def check_neighbours(map, x, y, marked_coords, plot_info):
    """Check neighbours recursively, mark as checked and update plot_info."""
    if x < 0 or x >= len(map[0]) or y < 0 or y >= len(map):
        return False
    marked_coord_id = y * len(map[0]) + x
    #print(f"Pre check {x},{y}, {plot_info['id']}")
    if marked_coord_id in  marked_coords:
        return True
    if map[y][x] != plot_info['id']:
        return False
    # Valid plot
    print(f"{x},{y} valid plot for {plot_info['id']}")
    marked_coords.append(marked_coord_id)
    plot_info['area'] += 1
    adj_coords = [{'x': x - 1, 'y': y}, {'x': x, 'y': y - 1}, {'x': x + 1, 'y': y}, {'x': x, 'y': y + 1}]
    # Check left, up, down, right and calculate perimeter
    for coords in adj_coords:
        if not check_neighbours(map, coords['x'], coords['y'], marked_coords, plot_info):
            #print(f"Perimiter check for {coords}")
            plot_info['perimeter'] += 1
    return True

def find_plot(map, marked_map, plots):
    """Find plot (same letter), mark on marked_map and add to plots."""
    found = False
    # Find next plot to calculate
    for y in range(len(marked_map)):
        for x in range(len(marked_map[0])):
            if marked_map[y][x] != 'x':
                marked_coords = []
                plot_info = {'id': map[y][x], 'area': 0, 'perimeter': 0}
                check_neighbours(map, x, y, marked_coords, plot_info)
                plots.append(plot_info)
                #print(plot_info)
                for coords in marked_coords:
                    y_mark = coords // len(map[0])
                    x_mark = coords % len(map[0])
                    marked_map[y_mark][x_mark] = 'x'
                #print(marked_map)
                found = True

    return found


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
            col.append(char)
        map.append(col)

    print_map(map)

    # Make a marked map
    marked_map = []
    for row in map:
        new_row = []
        for i in range(len(row)):
            new_row.append('.')
        marked_map.append(new_row)
    
    print(marked_map)

    if args.second:
        print(f"")
    else:
        found = True
        plots = []
        while(found):
            found = find_plot(map, marked_map, plots)
        price_sum = 0
        for plot in plots:
            price = plot['area'] * plot['perimeter']
            print(f"Region {plot['id']} - price {plot['area']} * {plot['perimeter']} = {price}")
            price_sum += price
        print(f"Total price: {price_sum}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
