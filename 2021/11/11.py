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


def print_table(rows):
    """Print rows."""
    for row in rows:
        line = ""
        for c in row:
            line += chr(c[0] + 0x30)
        print(line)
    print("\n")


def flash(rows, x, y):
    """Trigger flash."""
    if x > 0:
        rows[y][x - 1][0] += 1  # left
    if y > 0:
        rows[y - 1][x][0] += 1  # up
    if x > 0 and y > 0:
        rows[y - 1][x - 1][0] += 1  # left up
    if x < len(rows[0]) - 1:
        rows[y][x + 1][0] += 1  # right
    if y < len(rows) - 1:
        rows[y + 1][x][0] += 1  # down
    if x < len(rows[0]) - 1 and y < len(rows) - 1:
        rows[y + 1][x + 1][0] += 1  # right down
    if x > 0 and y < len(rows) - 1:
        rows[y + 1][x - 1][0] += 1  # left down
    if y > 0 and x < len(rows[0]) - 1:
        rows[y - 1][x + 1][0] += 1  # right up

    rows[y][x][1] = True


def flash_check(rows):
    """Check and count dumbo flashes."""
    count = 0
    for y in range(0, len(rows)):
        for x in range(0, len(rows[y])):
            if rows[y][x][0] > 9 and not rows[y][x][1]:
                flash(rows, x, y)
                count += 1

    return count


def main():
    """Main program."""
    args = get_args()

    rows = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                line = line.strip("\n\r")
                row = []
                for c in line:
                    row.append([int(c), False])
                rows.append(row)
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print_table(rows)
    flash_count = 0
    if not args.second:
        for step in range(0, 100):
            print(f"Step {step + 1}")
            # Increase all values by 1
            for row in rows:
                for n in range(0, len(row)):
                    row[n][0] += 1
            print_table(rows)
            count = 1
            while count > 0:
                count = flash_check(rows)
                flash_count += count

            # Reset flash flag
            for row in rows:
                for c in row:
                    if c[1]:
                        c[0] = 0
                        c[1] = False

            print_table(rows)

        print(f"Answer: {flash_count}")
    else:
        step = 0
        flash_count = 0
        while flash_count != 100:
            # Increase all values by 1
            for row in rows:
                for n in range(0, len(row)):
                    row[n][0] += 1
            while flash_check(rows) > 0:
                continue

            # Count flashes
            flash_count = 0
            for row in rows:
                for c in row:
                    if c[1]:
                        flash_count += 1

            # Reset flash flag
            for row in rows:
                for c in row:
                    if c[1]:
                        c[0] = 0
                        c[1] = False

            step += 1
            print(f"Step {step}")
            print_table(rows)

        print(f"Answer: {step}")
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
