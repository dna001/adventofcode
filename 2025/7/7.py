#!/usr/bin/env python3
"""
AdventOfCode day 7.
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

    # Read input
    try:
        with open(args.input, 'rt') as file:
            lines = file.readlines()
    except IOError:
        print("Failed reading file!")
        sys.exit()

    diagram = []
    for line in lines:
        tmp = line.strip('\n')
        row = []
        for c in line:
            row.append(c)
        diagram.append(row)

    if args.second:
        num_time_splits = 0
        beams = {}
        for x in range(len(diagram[0])):
            if diagram[0][x] == 'S':
                beams[str(x)] = 1
            else:
                beams[str(x)] = 0
                
        print(beams)
        for y in range(2, len(diagram), 2):
            row = diagram[y]
            # Find all splitters in current row
            for x in range(len(row)):
                if row[x] == '^':
                    if str(x) in beams.keys():
                        num_beams = beams[str(x)]
                        beams[str(x)] = 0
                        a = x - 1
                        b = x + 1
                        beams[str(a)] += num_beams
                        beams[str(b)] += num_beams

            print("-------------")
            print(beams)

        answer = 0
        for b in beams.values():
            answer += b

        print(f'Answer {answer}')
    else:
        num_splits = 0
        beams = []
        for x in range(len(diagram[0])):
            if diagram[0][x] == 'S':
                beams.append(x)
                break

        print(beams)
        for y in range(2, len(diagram), 2):
            row = diagram[y]
            # Find all splitters in current row
            for x in range(len(row)):
                if row[x] == '^':
                    if x in beams:
                        num_splits += 1
                        beams.remove(x)
                        a = x - 1
                        b = x + 1
                        if a not in beams:
                            beams.append(a)
                        if b not in beams:
                            beams.append(b)
            
        print(f'Answer {num_splits}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
