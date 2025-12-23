#!/usr/bin/env python3
"""
AdventOfCode day 15.
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
    turn = 0

    if not args.second:
        end_turn = 2020
    else:
        end_turn = 30000000

    numbers = [0] * end_turn
    numbers_last_0 = [-1] * end_turn
    numbers_last_1 = [-1] * end_turn

    # Read input
    try:
        with open(args.input, 'rt') as file:
            chunks = file.readline().strip('\n\r').split(',')
            for chunk in chunks:
                numbers[turn] = int(chunk)
                numbers_last_1[int(chunk)] = turn
                turn += 1

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(numbers[0: turn])
    print(numbers_last_0[0: 20])
    print(numbers_last_1[0: 20])

    start_time = datetime.now()

    while turn < end_turn:
        # Find previous number
        found = False
        old_num = numbers[turn - 1]
        #print("old_num: {}".format(old_num))
        #print(numbers_last[old_num][0])
        if numbers_last_0[old_num] >= 0:
            val = (turn - 1) - numbers_last_0[old_num]
        else:
            val = 0

        #print(val)

        numbers[turn] = val
        numbers_last_0[val] = numbers_last_1[val]
        numbers_last_1[val] = turn

        if turn % 10000 == 0:
            current = datetime.now() - start_time
            print("Turn: {} time: {} s".format(turn, current))
        turn += 1

    print(numbers[0: 20])
    print(numbers_last_0[0: 20])
    print(numbers_last_1[0: 20])
    #print(numbers)

    print("Number {}: {}".format(end_turn, numbers[-1]))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
