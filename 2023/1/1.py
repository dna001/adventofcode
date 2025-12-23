#!/usr/bin/env python3
"""
AdventOfCode day 1.
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
    cal_value_sum = 0

    # Read input
    try:
        with open(args.input, 'rt') as file:
            lines = file.readlines()
    except IOError:
        print("Failed reading file!")
        sys.exit()

    digit_lookup = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}

    if args.second:
        for line in lines:
            line = line.strip('\n')
            first = -1
            last = -1
            letter_start_index = 0
            letter_count = 0
            for i in range(0, len(line)):
                c = line[i]
                if (c >= '0') and (c <= '9'):
                    letter_count = 0
                    if first < 0:
                        first = int(c);
                    else:
                        last = int(c)
                else:
                    if letter_count == 0:
                        letter_start_index = i
                    letter_count += 1
                    if letter_count >=3:
                        word = line[letter_start_index:letter_start_index + letter_count]
                        print(f"{word}")
                        # Check for valid word:
                        for key in digit_lookup.keys():
                            if key in word:
                                print("hit")
                                if first < 0:
                                    first = digit_lookup[key];
                                else:
                                    last = digit_lookup[key]
                                letter_start_index += len(word) - 1
                                letter_count -= len(word) - 1

            if last < 0:
                last = first

            print(f"first:{first}, last:{last}")
            cal_value_sum += first * 10 + last

    else:
        for line in lines:
            line = line.strip('\n')
            first = -1
            last = -1
            for i in range(0, len(line)):
                c = line[i]
                if (c >= '0') and (c <= '9'):
                    if first < 0:
                        first = int(c);
                    else:
                        last = int(c)
            if last < 0:
                last = first

            print(f"first:{first}, last:{last}")
            cal_value_sum += first * 10 + last

    print(f"cal sum: {cal_value_sum}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
