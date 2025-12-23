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


def parse_boarding_pass(line):
    """Parse boarding pass."""
    row = 0
    col = 0
    seat_id = 0

    #print(line + '\n')
    for pos in range(0, len(line)):
        # 0 - 6 row
        if pos < 7:
            row = row << 1
            if line[pos] == 'B':
                row += 1
        # 7 - 9 col
        elif pos < 10:
            col = col << 1
            if line[pos] == 'R':
                col += 1

    seat_id = row * 8 + col
    print("Boarding pass: row {} col {} seat id {}".format(row, col, seat_id))

    return seat_id


def main():
    """Main program."""
    args = get_args()
    total_boarding_pass = 0
    id_seat_max = 0
    id_seats = []

    for pos in range(0, 127 * 8 + 7):
        id_seats.append(pos)

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                line = line.strip('\n\r')
                if len(line) > 0:
                    seat_id = parse_boarding_pass(line)
                    if seat_id > id_seat_max:
                        id_seat_max = seat_id
                    id_seats.remove(seat_id)
                    total_boarding_pass += 1
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print("Max seat id: {} ({})".format(id_seat_max, total_boarding_pass))
    print(id_seats)
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
