#!/usr/bin/env python3
"""
AdventOfCode day 17.
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


def find_cube(grid, x, y, z):
    """Find active cube in grid."""
    for cube in grid:
        if cube['x'] == x and cube['y'] == y and cube['z'] == z:
            return True

    return False


def check_neighbours(grid, x, y, z):
    """Check state of neighbours and set new state."""
    active = 0
    active_count = 0

    for x_new in range(x - 1, x + 2):
        for y_new in range(y - 1, y + 2):
            for z_new in range(z - 1, z + 2):
                if x_new == x and y_new == y and z_new == z:
                    if find_cube(grid, x_new, y_new, z_new):
                        active = 1
                elif find_cube(grid, x_new, y_new, z_new):
                    active_count += 1

    if active == 1 and (active_count == 2 or active_count == 3):
        new_state = 1
    elif active == 1:
        new_state = 0
    elif active == 0 and active_count == 3:
        new_state = 1
    else:
        new_state = 0

    #print("Active neigbours of [{}][{}][{}]: {}  {} -> {}".format(x, y, z, active_count, active, new_state))

    return new_state


def main():
    """Main program."""
    args = get_args()
    total_cycles = 6

    active_cubes = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            z = 0
            y = 0
            for line in file:
                line = line.strip('\n\r')
                x = 0
                for char in line:
                    if char == '#':
                        active_cubes.append({'x': x, 'y': y, 'z': z})
                    x += 1
                y += 1

    except IOError:
        print("Failed reading file!")
        sys.exit()

    # Find max size of active grid
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    min_z = 0
    max_z = 0
    for cube in active_cubes:
        if cube['x'] < min_x:
            min_x = cube['x']
        if cube['x'] > max_x:
            max_x = cube['x']
        if cube['y'] < min_y:
            min_y = cube['y']
        if cube['y'] > max_y:
            max_y = cube['y']
        if cube['z'] < min_z:
            min_z = cube['z']
        if cube['z'] > max_z:
            max_z = cube['z']

    print(active_cubes)

    start_time = datetime.now()

    count = 0
    while count < total_cycles:
        active_cubes_new = []
        for z in range(min_z - 1, max_z + 2):
            for y in range(min_y - 1, max_y + 2):
                for x in range(min_x - 1, max_x + 2):
                    #print("{} {} {}".format(x, y, z))
                    if check_neighbours(active_cubes, x, y, z) == 1:
                        active_cubes_new.append({'x': x, 'y': y, 'z': z})
  
        active_cubes = active_cubes_new
        # Find max size of active grid
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        min_z = 0
        max_z = 0
        for cube in active_cubes:
            if cube['x'] < min_x:
                min_x = cube['x']
            if cube['x'] > max_x:
                max_x = cube['x']
            if cube['y'] < min_y:
                min_y = cube['y']
            if cube['y'] > max_y:
                max_y = cube['y']
            if cube['z'] < min_z:
                min_z = cube['z']
            if cube['z'] > max_z:
                max_z = cube['z']

        pprint(active_cubes)
        print("Grid size x[{}->{}] y[{}->{}] z[{}->{}]".format(min_x, max_x, min_y, max_y, min_z, max_z))
        print("Grid active count: {}".format(len(active_cubes)))
        count += 1

    print("Active cubes in grid: {}".format(len(active_cubes)))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
