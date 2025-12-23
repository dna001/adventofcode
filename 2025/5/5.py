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


def sort_by_range_size(r):
    """ Sort by range size. """
    return r['stop'] - r['start']


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

    ranges = []
    parse_ranges = True
    ingredients = []
    for line in lines:
        tmp = line.strip('\n')
        if len(tmp) == 0:
            parse_ranges = False
            continue
        if parse_ranges:
            tmp_ranges = tmp.split('-')
            ranges.append({'start': int(tmp_ranges[0]), 'stop': int(tmp_ranges[1])})
        else:
            ingredients.append(int(tmp))

    print(ranges)
    print(ingredients)
        
    if args.second:
        answer = 0
        new_ranges = []

        ranges.sort(key=sort_by_range_size)
        ranges.reverse()
        print(ranges)
        for r in ranges:
            test_r = r.copy()
            if len(new_ranges) == 0:
                new_ranges.append(r)
                continue
            found = False
            for new_range in new_ranges:
                if test_r['start'] >= new_range['start'] and test_r['stop'] <= new_range['stop']:
                    found = True
                    break
                elif test_r['stop'] < new_range['start']:
                    continue
                elif test_r['start'] > new_range['stop']:
                    continue
                elif test_r['start'] < new_range['start'] and test_r['stop'] <= new_range['stop']:
                    # Add new range below
                    test_r['stop'] = new_range['start'] - 1
                elif test_r['start'] > new_range['start'] and test_r['stop'] > new_range['stop']:
                    # Add new range above
                    test_r['start'] = new_range['stop'] + 1
            
            if not found:
                new_ranges.append(test_r)

        print(new_ranges)
        # Count individual ranges
        for r in new_ranges:
            answer += r['stop'] - r['start'] + 1

        print(f'Answer {answer}')
    else:
        fresh = []
        for range in ranges:
            for ingredient in ingredients:
                if ingredient >= range['start'] and ingredient <= range['stop']:
                    if ingredient not in fresh:
                        fresh.append(ingredient)

        #print(answer)
        print(f'Answer {len(fresh)}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
