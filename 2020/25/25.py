#!/usr/bin/env python3
"""
AdventOfCode day 25.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
from pprint import pprint
from enum import Enum


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


def calc_loop_size(key):
    """Calculate loop size."""
    val = 1
    loop_size = 0
    while val != key:
        val *= 7
        val = val % 20201227
        loop_size += 1

    return loop_size


def calc_key(sn, loop_size):
    """Calculate encryption key."""
    enc_key = 1
    for count in range(0, loop_size):
        enc_key *= sn
        enc_key = enc_key % 20201227

    return enc_key


def main():
    """Main program."""
    args = get_args()

    card_key = 0
    door_key = 0

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            card_key = int(line.strip('\n\r'))
            line = file.readline()
            door_key = int(line.strip('\n\r'))

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print("Card key: {}".format(card_key))
    print("Door key: {}".format(door_key))

    card_loop_size = calc_loop_size(card_key)
    door_loop_size = calc_loop_size(door_key)

    encryption_key = calc_key(card_key, door_loop_size)
    print("Encryption key: {} card/door loop size {}/{}".format(encryption_key, card_loop_size, door_loop_size))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
