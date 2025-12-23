#!/usr/bin/env python3
"""
AdventOfCode day 8.
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


def main():
    """Main program."""
    args = get_args()
    crab_positions = []

    segment_output = []
    min_pos = sys.maxsize
    max_pos = 0

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                input_output = line.strip("\n\r").split(' | ')
                segments = []
                for seg in input_output[1].split(' '):
                    segments.append(seg.strip(' '))
                segment_output.append(segments)
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(segment_output)

    count = 0
    for segments in segment_output:
        # Count digits 1, 4, 7, 8
        for segment in segments:
            if len(segment) == 2 or len(segment) == 3 or len(segment) == 4 or len(segment) == 7:
                count += 1

    print(f"Answer: {count}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
