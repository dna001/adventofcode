#!/usr/bin/env python3
"""
AdventOfCode day 14.
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
    masks = []
    memory = {}
    mask_count = -1

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline().strip('\n\r')
            while len(line) > 0:
                if 'mask' in line:
                    mask_count += 1
                    masks.append({})
                    mask_or = 0
                    mask_and = 0
                    for char in line[7:]:
                        mask_or = mask_or << 1
                        mask_and = mask_and << 1
                        if char == 'X':
                            mask_and += 1
                        elif char == '1':
                            mask_or += 1
                            mask_and += 1

                    masks[mask_count]['mask_or'] = mask_or
                    masks[mask_count]['mask_and'] = mask_and
                    masks[mask_count]['mem'] = []
                elif 'mem' in line:
                    start = line.find('[')
                    stop = line.find(']')
                    addr = int(line[start + 1:stop])
                    start = line.find('=')
                    val = int(line[start + 2:])
                    masks[mask_count]['mem'].append({'addr': addr, 'val': val})

                line = file.readline().strip('\n\r')

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(masks)

    for mask in masks:
        mask_or = mask['mask_or']
        mask_and = mask['mask_and']
        for mem in mask['mem']:
            print(mem)
            if mem['addr'] not in memory:
                memory[mem['addr']] = 0
            val = (mem['val'] | mask_or) & mask_and
            memory[mem['addr']] = val
    
    print(memory)

    summary = 0
    for mem, val in memory.items():
        summary += val

    print("Answer {}".format(summary))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
