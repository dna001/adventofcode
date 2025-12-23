#!/usr/bin/env python3
"""
AdventOfCode day 2.
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

    lines[0].strip('\n')
    ranges = lines[0].split(',')
    range_pairs = []
    for r in ranges:
        pair = r.split('-')
        range_pairs.append(pair)

    print(ranges)

    if args.second:
        answer = 0
        for pair in range_pairs:
            start = int(pair[0])
            stop = int(pair[1]) + 1
            for i in range(start, stop):
                str_val = str(i)
                if len(str_val) == 1:
                    continue
                digits_to_check = []
                digits_to_check.append(1)
                # Check all lengths that is evenly diveded by length of string
                for j in range(2, (len(str_val) // 2) + 1):
                    if len(str_val) / j == len(str_val) // j:
                        digits_to_check.append(j)

                #print(digits_to_check)

                for n_digits in digits_to_check:
                    val_to_check = str_val[0:n_digits]
                    same = 0
                    for j in range(n_digits, len(str_val) + 1, n_digits):
                        #print(j)
                        if val_to_check == str_val[j: j + n_digits]:
                            #print(f"found match {str_val}")
                            same += 1

                    if same == len(str_val) // n_digits - 1:
                        print(f"invalid id {str_val}")
                        answer += i
                        break

        print(f'Answer {answer}')
    else:
        answer = 0
        for pair in range_pairs:
            start = int(pair[0])
            stop = int(pair[1]) + 1
            for i in range(start, stop):
                str_val = str(i)
                if (len(str_val) % 2) == 0:
                    # Only check even digits
                    if str_val[0:len(str_val) // 2] == str_val[len(str_val) // 2:]:
                        print(f"invalid id {str_val}")
                        answer += i

        print(f'Answer {answer}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
