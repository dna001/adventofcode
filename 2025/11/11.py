#!/usr/bin/env python3
"""
AdventOfCode day 11.
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


def find_path(devices, start, end, info):
    """ Find number of paths from start to end. """
    if start not in devices:
        #print(f'{start} not found')
        return
    first = devices[start]
    for device in first:
        #print(device)
        if device in info['path']:
            print(f'loop: {info['path']}')
            continue
        if device == end:
            print(info['path'])
            #print(f'Found path in {start}')
            info['count'] += 1
            continue
        else:
            info['path'].append(device)
            find_path(devices, device, end, info)
            del info['path'][-1]


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

    devices = {}
    for line in lines:
        tmp = line.strip('\n')
        tmp = tmp.split(':')
        devices[tmp[0]] = tmp[1].split(' ')[1:]

    print(devices)

    info = {'count': 0, 'path': []}
    if args.second:
        answer = 0
        #find_path(devices, 'svr', 'out', info)
        #print(f'svr -> out: {info['count']}')
        info['count'] = 0
        info['path'] = []
        find_path(devices, 'svr', 'fft', info)
        print(f'svr -> fft: {info['count']}')
        svr_fft = info['count']
        info['count'] = 0
        info['path'] = []
        #find_path(devices, 'fft', 'dac', info)
        #print(f'fft -> dac: {info['count']}')
        fft_dac = info['count']
        info['count'] = 0
        info['path'] = []
        find_path(devices, 'dac', 'out', info)
        print(f'dac -> out: {info['count']}')
        dac_out = info['count']

        answer = svr_fft * fft_dac * dac_out
        print(f'Answer {answer}')
    else:
        answer = 0
        find_path(devices, 'you', 'out', info)
        answer = info['count']
        print(f'Answer {answer}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
