#!/usr/bin/env python3
"""
AdventOfCode day 11.
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

def check_direction(seat_rows, row, seat, dir_x, dir_y, second):
    """Find occupied seat in direction dir_x/dir_y."""
    found = False
    current_row = row + dir_y
    current_seat = seat + dir_x

    while not found and current_row >= 0 and current_row < len(seat_rows) and \
        current_seat >= 0 and current_seat < len(seat_rows[0]):
        if seat_rows[current_row][current_seat] == '#':
            found = True
        if not second:
            break
        else:
            if seat_rows[current_row][current_seat] == 'L':
                break
            current_row += dir_y
            current_seat += dir_x

    return found

def count_adjacent(seat_rows, row, seat, second):
    """Count occupied adjacent seats."""
    count = 0
    # 123
    # 4x5
    # 678
    if check_direction(seat_rows, row, seat, -1, -1, second): # Up, Left (1)
        count +=1
    if check_direction(seat_rows, row, seat, 0, -1, second): # Up (2)
        count +=1
    if check_direction(seat_rows, row, seat, 1, -1, second): # Up, Right (3)
        count +=1
    if check_direction(seat_rows, row, seat, -1, 0, second): # Left (4)
        count +=1
    if check_direction(seat_rows, row, seat, 1, 0, second): # Right (5)
        count +=1
    if check_direction(seat_rows, row, seat, -1, 1, second): # Down, Left (6)
        count +=1
    if check_direction(seat_rows, row, seat, 0, 1, second): # Down (7)
        count +=1
    if check_direction(seat_rows, row, seat, 1, 1, second): # Down, Right (8)
        count +=1

    return count


def run_seat_allocation(seat_rows, second):
    """Run seat allocation."""
    runs = 0
    new_seat_rows = []
    equal = False

    if not second:
        adjacent_limit = 4
    else:
        adjacent_limit = 5

    while not equal:
        new_seat_rows = seat_rows.copy()
        for row in range(0, len(seat_rows)):
            row_text = ""
            for seat in range(0, len(seat_rows[0])):
                # Empty seat
                if seat_rows[row][seat] == 'L':
                    adjacent = count_adjacent(seat_rows, row, seat, second)
                    if adjacent == 0:
                        row_text += '#'
                    else:
                        row_text += 'L'
                elif seat_rows[row][seat] == '#':
                    adjacent = count_adjacent(seat_rows, row, seat, second)
                    if adjacent >= adjacent_limit:
                        row_text += 'L'
                    else:
                        row_text += '#'
                else:
                    row_text += '.'

            new_seat_rows[row] = row_text

        equal = True
        for row in range(0, len(seat_rows)):
            if seat_rows[row] not in new_seat_rows[row]:
                equal = False
                break

        for row in new_seat_rows:
            print(row)

        seat_rows = new_seat_rows
        runs += 1
        #if runs == 2:
        #    break

    seats = 0
    # Count seats
    for row in seat_rows:
        for seat in row:
            if seat == "#":
                seats += 1

    return (seats, runs)


def main():
    """Main program."""
    args = get_args()
    total_rows = 0
    seat_rows = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                line = line.strip('\n\r')
                seat_rows.append(line)
                total_rows += 1
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    for row in seat_rows:
        print(row)

    seats, runs = run_seat_allocation(seat_rows, args.second)

    print("{} seats allocated after {} runs (total rows: {})".format(seats, runs, total_rows))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
