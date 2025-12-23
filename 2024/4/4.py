#!/usr/bin/env python3
"""
AdventOfCode day 4.
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

def count_xmas_in_lines(lines):
    """Count number of times XMAS occurs in lines."""
    count = 0
    for line in lines:
        pos = 0
        while (pos >= 0):
            pos = line.find("XMAS", pos)
            if pos >= 0:
                count += 1
                pos += 4
    print(f"Sub count {count}")
    return count

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

    for line in lines:
        line = line.strip('\n')

    if args.second:
        # X-MAS
        # M M S S
        #  A   A
        # S S M M
        xmas_count = 0
        for y in range(0, len(lines)):
            for x in range(0, len(line)):
                if lines[y][x] == 'A':
                    # Search for MAS or SAM
                    if x >= 1 and x < len(line) - 1 and y >= 1 and y < len(lines) - 1:
                        tl_br = lines[y - 1][x - 1] + lines[y][x] + lines[y + 1][x + 1]
                        bl_tr = lines[y + 1][x - 1] + lines[y][x] + lines[y - 1][x + 1]
                        if (tl_br == "MAS" or tl_br == "SAM") and (bl_tr == "MAS" or bl_tr == "SAM"):
                            xmas_count += 1
                            print(f"Found X-MAS at {x},{y}")

            print(f"X-MAS count at line {y} = {xmas_count}")

        print(f'Total X-MAS count: {xmas_count}')
    else:
        xmas_count = 0
        for y in range(0, len(lines)):
            for x in range(0, len(line)):
                if lines[y][x] == 'X':
                    # Search for XMAS in all directions
                    # Search left to right
                    if x <= len(lines) - 4:
                        lr = lines[y][x: x + 4]
                        if lr == "XMAS":
                            xmas_count += 1
                            print("Found lr")
                    # Search right to left
                    if x >= 3:
                        rl = lines[y][x] + lines[y][x - 1] + lines[y][x - 2] + lines[y][x - 3]
                        if rl == "XMAS":
                            xmas_count += 1
                            print("Found rl")
                    # Search bottom to top
                    if y >= 3:
                        up = lines[y][x] + lines[y - 1][x] + lines[y - 2][x] + lines[y - 3][x]
                        if up == "XMAS":
                            xmas_count += 1
                            print("Found bt")
                    # Search top to bottom
                    if y <= len(lines) - 4:
                        down = lines[y][x] + lines[y + 1][x] + lines[y + 2][x] + lines[y + 3][x]
                        if down == "XMAS":
                            xmas_count += 1
                            print("Found tb")
                    # Search diagonal top left to bottom right
                    if x <= len(line) - 4 and y <= len(lines) - 4:
                        tl_to_br = lines[y][x] + lines[y + 1][x + 1] + lines[y + 2][x + 2] + lines[y + 3][x + 3]
                        if tl_to_br == "XMAS":
                            xmas_count += 1
                            print("Found tl br")
                    # Search diagonal bottom right to top left
                    if x >= 3 and y >= 3:
                        br_to_tl = lines[y][x] + lines[y - 1][x - 1] + lines[y - 2][x - 2] + lines[y - 3][x - 3]
                        if br_to_tl == "XMAS":
                            xmas_count += 1
                            print("Found br tl")
                    # Search diagonal bottom left to top right
                    if x <= len(line) - 4 and y >= 3:
                        bl_to_tr = lines[y][x] + lines[y - 1][x + 1] + lines[y - 2][x + 2] + lines[y - 3][x + 3]
                        if bl_to_tr == "XMAS":
                            xmas_count += 1
                            print("Found bl tr")
                    # Search diagonal top right to bottom left
                    if x >= 3 and y <= len(lines) - 4:
                        tr_to_bl = lines[y][x] + lines[y + 1][x - 1] + lines[y + 2][x - 2] + lines[y + 3][x - 3]
                        if tr_to_bl == "XMAS":
                            xmas_count += 1
                            print("Found tr bl")

            print(f"XMAS count at line {y} = {xmas_count}")

        print(f'Total XMAS count: {xmas_count}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
