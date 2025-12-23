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


def get_dir(angle):
    """Get x, y direction from angle."""
    if angle == 0: # N
        dir_x = 0
        dir_y = -1
    elif angle == 90: # E
        dir_x = 1
        dir_y = 0
    elif angle == 180: # S
        dir_x = 0
        dir_y = 1
    elif angle == 270: # W
        dir_x = -1
        dir_y = 0

    return (dir_x, dir_y)


def run_nav(nav_steps):
    """Run navigation steps."""
    pos_x = 0
    pos_y = 0
    rotation = 90

    for step in nav_steps:
        move = True
        val = int(step[1:])

        if step[0] == 'F':
            move_x, move_y = get_dir(rotation)
        elif step[0] == 'N':
            move_x, move_y = get_dir(0)
        elif step[0] == 'E':
            move_x, move_y = get_dir(90)
        elif step[0] == 'S':
            move_x, move_y = get_dir(180)
        elif step[0] == 'W':
            move_x, move_y = get_dir(270)
        elif step[0] == 'L':
            val = -val
            move = False
        elif step[0] == 'R':
            move = False

        if move:
            move_x *= val
            move_y *= val
            pos_x += move_x
            pos_y += move_y
        else:
            rotation += val + 360
            rotation = rotation % 360

    return (pos_x, pos_y)


def rotate_waypoint(angle, x, y):
    """Rotate waypoint."""
    angle = (angle + 360) % 360
    if angle == 0:
        return x, y
    elif angle == 90:
        return -y, x
    elif angle == 180:
        return -x, -y
    elif angle == 270:
        return y, -x

    return (0, 0)


def run_nav_2(nav_steps):
    """Run navigation steps."""
    pos_x = 0
    pos_y = 0
    waypoint_x = 10
    waypoint_y = -1

    for step in nav_steps:
        move = True
        val = int(step[1:])

        if step[0] == 'F':
            pos_x += waypoint_x * val
            pos_y += waypoint_y * val
        elif step[0] == 'N':
            waypoint_y -= val
        elif step[0] == 'E':
            waypoint_x += val
        elif step[0] == 'S':
            waypoint_y += val
        elif step[0] == 'W':
            waypoint_x -= val
        elif step[0] == 'L':
            waypoint_x, waypoint_y = rotate_waypoint(-val, waypoint_x, waypoint_y)
        elif step[0] == 'R':
            waypoint_x, waypoint_y = rotate_waypoint(val, waypoint_x, waypoint_y)

        print("wpx: {} wpx: {} x: {} y: {}".format(waypoint_x, waypoint_y, pos_x, pos_y))

    return (pos_x, pos_y)


def main():
    """Main program."""
    args = get_args()
    total_lines = 0
    nav_steps = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                line = line.strip('\n\r')
                nav_steps.append(line)
                total_lines += 1
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    if not args.second:
        x, y = run_nav(nav_steps)
    else:
        x, y = run_nav_2(nav_steps)

    print("Position x: {} y: {} Manhattan distance: {}".format(x, y, abs(x) + abs(y)))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
