#!/usr/bin/env python3
"""
AdventOfCode day 5.
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


    result = 0
    seeds = []
    converter_map = []
    converter = {}
    for i in range(0, len(lines)):
        line = lines[i]
        if "seeds" in line:
            line_seeds = line.strip('\n').split(':')[1].split(' ')
            for seed in line_seeds:
                if seed:
                    seeds.append(int(seed))
        elif line[0] in 'sfwlth':
            converter = {'name': line.strip('\n')}
            converter['ranges'] = []
            converter_map.append(converter)
        elif line[0] in '0123456789':
            ranges = line.strip('\n').split(' ')
            converter['ranges'].append({'dst_start': int(ranges[0]), 'src_start': int(ranges[1]), 'range': int(ranges[2])})
    print(seeds)
    #print(converter_map)

    seed_locations = []
    for seed in seeds:
        # Find seed location
        new_value = seed
        for converter in converter_map:
            print(converter)
            search_value = new_value
            new_value = -1
            for r in converter['ranges']:
                if search_value >= r['src_start'] and search_value <= r['src_start'] + r['range']:
                    new_value = search_value - r['src_start'] + r['dst_start']
                    break
            if new_value < 0:
                new_value = search_value
            print(f"{converter['name']}: {search_value} -> {new_value}")
        seed_locations.append(new_value)
    seed_locations.sort()
    print(seed_locations)
    result = seed_locations[0]
    print(f"result: {result}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
