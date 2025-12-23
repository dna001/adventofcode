#!/usr/bin/env python3
"""
AdventOfCode day 6.
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


def walk_one_step(x, y, direction, map, mark_direction = False):
    """Walk one step on map and return position and direction or out of bounds."""
    new_direction = direction
    marker = 'X'
    if mark_direction:
        if direction == 'up' or direction == 'down':
            marker = '|'
        else:
            marker = '-'
    if direction == 'up':
        y -= 1
        if (y < 0):
            new_direction = 'done'
        else:
            if map[y][x] == '#':
                y += 1
                new_direction = 'right'
                if mark_direction:
                    map[y][x] = '+'
            else:
                map[y][x] = marker
    elif direction == 'right':
        x += 1
        if (x >= len(map[y])):
            new_direction = 'done'
        else:
            if map[y][x] == '#':
                x -= 1
                new_direction = 'down'
                if mark_direction:
                    map[y][x] = '+'
            else:
                map[y][x] = marker
    elif direction == 'down':
        y += 1
        if (y >= len(map)):
            new_direction = 'done'
        else:
            if map[y][x] == '#':
                y -= 1
                new_direction = 'left'
                if mark_direction:
                    map[y][x] = '+'
            else:
                map[y][x] = marker
    elif direction == 'left':
        x -= 1
        if (x >= len(map)):
            new_direction = 'done'
        else:
            if map[y][x] == '#':
                x += 1
                new_direction = 'up'
                if mark_direction:
                    map[y][x] = '+'
            else:
                map[y][x] = marker

    return {'x': x, 'y': y, 'direction': new_direction}


def print_map(map):
    """Print map."""
    for row in map:
        row_string = ""
        for char in row:
            row_string += char
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

    print_map(map)

    start_pos = {}
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == '^':
                start_pos = {'x': x, 'y': y}
                if not args.second:
                    map[y][x] = 'X'
    direction = 'up'
    print(start_pos)
    x = start_pos['x']
    y = start_pos['y']

    if args.second:
        # Find possible blocker locations for endless loops
        found_loop_positions = []
        turn_list = []
        while direction != 'done':
            new_direction_and_pos = walk_one_step(x, y, direction, map, True)
            if new_direction_and_pos['direction'] != direction:
                turn_list.append(new_direction_and_pos)
            x = new_direction_and_pos['x']
            y = new_direction_and_pos['y']
            direction = new_direction_and_pos['direction']
            if len(turn_list) >= 3 and direction != "done":
                #old_obstacle_pos_list = []
                #for i in range(0, len(turn_list) // 3):
                #    old_obstacle_pos_list.append(turn_list[i * -3])
                for old_obstacle_pos in turn_list:
                    # Find out if line to 3:d last turn obstacle is clear of obstacles
                    #print(old_obstacle_pos)
                    found = True
                    obstacle_pos_x = 0
                    obstacle_pos_y = 0
                    if direction == "up" and old_obstacle_pos['x'] > x and old_obstacle_pos['y'] == y:
                        for check_x in range(x, old_obstacle_pos['x']):
                            if map[y][check_x] == "#":
                                found = False
                                break
                        obstacle_pos_x = x
                        obstacle_pos_y = y - 1
                    elif direction == "right" and old_obstacle_pos['y'] > y and old_obstacle_pos['x'] == x:
                        for check_y in range(y, old_obstacle_pos['y']):
                            if map[check_y][x] == "#":
                                found = False
                                break
                        obstacle_pos_x = x + 1
                        obstacle_pos_y = y
                    elif direction == "down" and old_obstacle_pos['x'] < x and old_obstacle_pos['y'] == y:
                        for check_x in range(old_obstacle_pos['x'], x):
                            if map[y][check_x] == "#":
                                found = False
                                break
                        obstacle_pos_x = x
                        obstacle_pos_y = y + 1
                    elif direction == "left" and old_obstacle_pos['y'] < y and old_obstacle_pos['x'] == x:
                        for check_y in range(old_obstacle_pos['y'], y):
                            if map[check_y][x] == "#":
                                found = False
                                break
                        obstacle_pos_x = x - 1
                        obstacle_pos_y = y
                    else:
                        found = False
                    if found and obstacle_pos_x >= 0 and obstacle_pos_y >= 0:
                        print(f"Obstacle pos {obstacle_pos_x}, {obstacle_pos_y}")
                        obstacle_pos_state = map[obstacle_pos_y][obstacle_pos_x]
                        if obstacle_pos_state == '|' or obstacle_pos_state == '-' or obstacle_pos_state == '+':
                            found = False
                        if found:
                            found_loop_positions.append(new_direction_and_pos)
                            print(f"Found loop pos at {x}, {y}, dir: {direction}")
                            old_state = map[obstacle_pos_y][obstacle_pos_x]
                            map[obstacle_pos_y][obstacle_pos_x] = 'O'
                            print("Map after guard walk and obstacle placement")
                            print_map(map)
                            map[obstacle_pos_y][obstacle_pos_x] = old_state

        print(f"N loop positions found: {len(found_loop_positions)}")

    else:
        # Find all positions the guard will walk on until it leaves the map
        while direction != 'done':
            new_direction_and_pos = walk_one_step(x, y, direction, map)
            x = new_direction_and_pos['x']
            y = new_direction_and_pos['y']
            direction = new_direction_and_pos['direction']

        print("Map after guard walk")
        print_map(map)

        x_count = 0
        # Count X:s
        for row in map:
            for col in row:
                if col == 'X':
                    x_count += 1
        print(f"X count: {x_count}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
