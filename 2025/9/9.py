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


def sort_by_area(r):
    """ Sort by area. """
    return r['area']


def print_tiles(tiles):
    """ Print tiles. """
    if len(tiles) > 20:
        print("grid")
        return
    print("-----")
    for row in tiles:
        row_str = ""
        for tile in row:
            for i in range(32):
                if tile & (1 << (31 - i)):
                    row_str += '#'
                else:
                    row_str += '.'
        print(row_str)


def set_grid(grid, x, y, val):
    """ Set bit in grid. """
    val = grid[y][x // 32]
    grid[y][x // 32] = val | (1 << (31 - (x % 32)))


def get_grid(grid, x, y):
    """ Get bit in grid. """
    val = grid[y][x // 32] & (1 << (31 - (x % 32)))
    return val != 0


def find_adjacent(grid, x, y):
    """ Find adjacent non filled tiles. """
    adj = []
    if not get_grid(grid, x - 1, y):
        adj.append([x - 1, y])
    if not get_grid(grid, x + 1, y):
        adj.append([x + 1, y])
    if not get_grid(grid, x, y - 1):
        adj.append([x, y - 1])
    if not get_grid(grid, x, y + 1):
        adj.append([x, y + 1])
    
    return adj


def fill_center(grid, x, y):
    """ Fill middle with green. """
    filled = False
    adjacent = find_adjacent(grid, x, y)
    while len(adjacent) > 0:
        new_adjacent_list = []
        for c in adjacent:
            set_grid(grid, c[0], c[1], 1)
            #grid[c[1]][c[0]] = 'X'
            adj = find_adjacent(grid, c[0], c[1])
            if len(adj) > 0:
                new_adjacent_list.extend(adj)

        adjacent = new_adjacent_list.copy()


def old_grid_stuff(coords, max_x, max_y):
    """ Old grid stuff. """
    grid = []
    for i in range(max_y + 2):
        row = [0] * ((max_x + 2) // 32 + 1)
        grid.append(row)
    
    print_tiles(grid)

    # Add red tiles
    for c in coords:
        set_grid(grid, c[0], c[1], 1)
        #grid[c[1]][c[0]] = '#'

    # Draw green lines
    for i in range(len(coords)):
        x1 = coords[i][0]
        x2 = coords[(i + 1) % len(coords)][0]
        y1 = coords[i][1]
        y2 = coords[(i + 1) % len(coords)][1]
        print(f'{x1},{y1} -> {x2}, {y2}')
        # Draw vertical line
        if x1 == x2:
            if y1 > y2:
                tmp = y2
                y2 = y1
                y1 = tmp
            for y in range(y1 + 1, y2):
                set_grid(grid, x1, y, 1)
                #grid[y][x1] = 'X'
        # Draw horizontal line
        elif y1 == y2:
            if x1 > x2:
                tmp = x2
                x2 = x1
                x1 = tmp
            for x in range(x1 + 1, x2):
                set_grid(grid, x, y1, 1)
                #grid[y1][x] = 'X'

    print_tiles(grid)

    # Find coordinate inside "fence"
    start_x = len(grid) // 2
    start_y = len(grid) // 2

    print(f'Start: {start_x},{start_y}')
    # Fill center
    fill_center(grid, start_x, start_y)
    print_tiles(grid)


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

    coords = []
    for line in lines:
        tmp = line.strip('\n')
        coord = []
        coord_tuple = tmp.split(',')
        coord.append(int(coord_tuple[0]))
        coord.append(int(coord_tuple[1]))
        coords.append(coord)

    print(coords)

    area_list = []
    for i in range(len(coords)):
        c = coords[i]
        for j in range(i + 1, len(coords)):
            c2 = coords[j]
            area = (abs(c2[0] - c[0]) + 1) * (abs(c2[1] - c[1]) + 1)
            area_list.append({'a': i, 'b': j, 'area': area})

    print(area_list[:10])

    area_list.sort(key=sort_by_area)
    area_list.reverse()
    print(area_list[:10])

    min_x = coords[0][0]
    min_y = coords[0][1]
    max_x = coords[0][0]
    max_y = coords[0][1]
    # Find min and max x and y values
    for c in coords:
        if min_x > c[0]:
            min_x = c[0]
        if max_x < c[0]:
            max_x = c[0]
        if min_y > c[1]:
            min_y = c[1]
        if max_y < c[1]:
            max_y = c[1]

    print(f'x range: {min_x}/{max_x}, y range: {min_y}/{max_y}')
    if args.second:
        answer = 0

        # Find largest area with filled tiles
        for area in area_list:
            # Check if all tiles filled
            x1 = coords[area['a']][0]
            y1 = coords[area['a']][1]
            x2 = coords[area['b']][0]
            y2 = coords[area['b']][1]
            if x1 > x2:
                tmp = x2
                x2 = x1
                x1 = tmp
            if y1 > y2:
                tmp = y2
                y2 = y1
                y1 = tmp

            top_right = [x2, y1]
            bottom_left = [x1, y2]
            filled = True
            print(f'{x1},{y1} -> {x2}, {y2} ({area['area']})')
            # Check if all coordinates within area
            for c in coords:
                if top_right[0] > c[0] or top_right[1] < c[1] or \
                   bottom_left[0] < c[0] or bottom_left[1] > c[1]:
                    print(f'top right: x {top_right[0]} > {c[0]}, y {top_right[1]} < {c[1]}')
                    print(f'bottom left: x {bottom_left[0]} < {c[0]}, y {bottom_left[1]} > {c[1]}')
                    filled = False
                    break

            if filled:
                answer = area['area']
                break

        print(f'Answer {answer}')
    else:
        answer = area_list[0]['area']
        print(f'Answer {answer}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
