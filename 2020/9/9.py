#!/usr/bin/env python3
"""
AdventOfCode day 9.
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


def find_bad_number(data, preamble):
    """Find bad number."""
    for number in range(preamble, len(data)):
        found = False
        for a in range(0, preamble - 1):
            for b in range(a + 1, preamble):
                num_a = data[number - preamble + a]
                num_b = data[number - preamble + b]
                #print("num_a: {} num_b: {}".format(num_a, num_b))
                if data[number] ==  num_a + num_b:
                    found = True
                    break
            if found:
                break
        if not found:
            return (number, data[number])

    return (0, 0)


def main():
    """Main program."""
    args = get_args()
    total_lines = 0
    data = []
    preamble = 25

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                line = line.strip('\n\r')
                data.append(int(line))
                total_lines += 1
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(data)

    pos, number = find_bad_number(data, preamble)

    print("Number {} at position {} is bad".format(number, pos))
    #input("Press any key to continue...")

    if args.second:
        for num in range(0, len(data)):
            tmp_num = 0
            tmp_pos = 0
            num_min = data[num]
            num_max = data[num]
            for pos in range(num, len(data)):
                tmp_num += data[pos]
                if data[pos] < num_min:
                    num_min = data[pos]
                if data[pos] > num_max:
                    num_max = data[pos]
                if tmp_num >= number:
                    break
            if tmp_num == number:
                print("tmp_num {} number {}".format(tmp_num, number))
                enc_weak = num_min + num_max
                break;

        print("Encryption weakness: {} (start: {} stop: {})".format(enc_weak, num, pos))


if __name__ == "__main__":
    main()
