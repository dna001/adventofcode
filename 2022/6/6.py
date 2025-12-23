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
import math


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


def main():
    """Main program."""
    args = get_args()
    message = ""

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            line.strip('\n')
            offs = 0
            marker = 0
            marker_old = 0
            print(line)
            for ch in line:
                # Skip first 3 chars
                if offs < 1:
                    offs += 1
                    continue
                if args.second:
                    if offs - marker >= 14:
                        # Marker found
                        marker = offs

                        print(f"Marker found")
                        break
                    search_str = line[max(offs - 13, 0): offs]
                    if ch in search_str:
                        new_marker = offs - len(search_str) + 1 + search_str.rfind(ch)
                        marker_old = marker
                        marker = max(marker, new_marker)
                else:
                    search_str = line[max(offs - 3, 0): offs]
                    if ch in search_str:
                        marker = offs - len(search_str) + 1 + search_str.rfind(ch)
                    if offs - marker >= 4:
                        # Marker found
                        marker = offs
                        print(f"Marker found")
                        break

                print(f"{search_str}:{ch}")
                print(marker)

                offs += 1
            print(f"Marker found at {marker}")

    except IOError:
        print("Failed reading file!")
        sys.exit()

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
