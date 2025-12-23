#!/usr/bin/env python3
"""
AdventOfCode day 13.
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
    depart_time = 0
    buses = ""
    depart_list = {}

    # Read input
    try:
        with open(args.input, 'rt') as file:
            depart_time = int(file.readline().strip('\n\r'))
            buses = file.readline().strip('\n\r').split(',')

    except IOError:
        print("Failed reading file!")
        sys.exit()

    for bus in buses:
        if bus != 'x':
            bus_id = int(bus)
            depart_list[bus] = (int(depart_time / bus_id) + 1) * bus_id


    print(depart_list)

    closest_time = 100
    bus_id = 0
    for bus, time in depart_list.items():
        if time - depart_time < closest_time:
            bus_id = bus
            closest_time = time - depart_time

    print("Depart time: {} Bus: {} Wait time: {} Answer {}".format(
        depart_time, bus_id, closest_time, int(bus_id) * closest_time))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
