#!/usr/bin/env python3
"""
AdventOfCode day 3.
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

    banks = []
    for line in lines:
        banks.append(line.strip('\n'))

    if args.second:
        answer = 0
        for bank in banks:
            bank_val = 0
            n = 0
            offset = 0
            most_left_offset = 0
            while n < 12:
                max_val = 0
                # Find largest joltage 
                for i in range(offset, len(bank) - (11 - n)):
                    val = int(bank[i])
                    if val > max_val:
                        max_val = val
                        most_left_offset = i
            
                offset = most_left_offset + 1
                bank_val = bank_val * 10 + max_val
                n += 1

            print(bank_val)
            answer += bank_val
        print(f'Answer {answer}')
    else:
        answer = 0
        for bank in banks:
            max_val = 0
            for i in range(len(bank) - 1):
                for j in range(i + 1, len(bank)):
                    val = int(bank[i]) * 10 + int(bank[j])
                    if val > max_val:
                        max_val = val
            print(max_val)
            answer += max_val

        print(f'Answer {answer}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
