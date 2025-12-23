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


def validate_password(line):
    """Validate password."""
    split = line.split(' ')
    min_times = int(split[0].split('-')[0])
    max_times = int(split[0].split('-')[1])
    char = split[1].strip(':')
    password = split[2]
    # Count char in password
    count = 0
    for ch in password:
        if ch == char:
            count += 1

    if count >= min_times and count <= max_times:
        return True
    else:
        print("{}-{} {}: {}".format(min_times, max_times, char, password))
        return False


def validate_password_2(line):
    """Validate password."""
    split = line.split(' ')
    pos1 = int(split[0].split('-')[0])
    pos2 = int(split[0].split('-')[1])
    char = split[1].strip(':')
    password = split[2]
    
    # Check character positions in password
    if password[pos1 - 1] == char and password[pos2 - 1] != char or \
       password[pos1 - 1] != char and password[pos2 - 1] == char:
        return True
    else:
        print("{}-{} {}: {}".format(pos1, pos2, char, password))
        return False


def main():
    """Main program."""
    args = get_args()
    lines = []
    policy_failures = 0
    total = 0

    # Read input
    #1-3 a: abcde
    #1-3 b: cdefg
    #2-9 c: ccccccccc    
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                if not args.second:
                    if not validate_password(line):
                        policy_failures += 1
                else:
                    if not validate_password_2(line):
                        policy_failures += 1
                total += 1
                line = file.readline()
    except IOError:
        print("Failed reading file!")
        sys.exit()

    print("Valid passwords: {}/{}".format(total - policy_failures, total))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
