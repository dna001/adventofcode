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

    # Read input
    try:
        with open(args.input, 'rt') as file:
            lines = file.readlines()
    except IOError:
        print("Failed reading file!")
        sys.exit()

    value_list_1 = []
    value_list_2 = []
    for line in lines:
        line = line.strip('\n')
        numbers = line.split('   ')
        value_list_1.append(int(numbers[0]))
        value_list_2.append(int(numbers[1]))

    if args.second:
        similatity_score_sum = 0
        # Calculate similatiry score (number in list 1 * number of times in list 2)
        for i in range(0, len(value_list_1)):
            num_vals = 0
            val = value_list_1[i]
            for value in value_list_2:
                if value == val:
                    num_vals += 1
            similatity_score_sum += val * num_vals
        
        print(f"similatory score sum: {similatity_score_sum}")

    else:
        dist_value_sum = 0
        value_list_1.sort()
        value_list_2.sort()
        print(f'{value_list_1}')
        print(f'{value_list_2}')
        for i in range(0, len(value_list_1)):
            dist_value_sum += abs(value_list_1[i] - value_list_2[i])

        print(f"distance sum: {dist_value_sum}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
