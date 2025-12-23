#!/usr/bin/env python3
"""
AdventOfCode day 7.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
import math

sum_of_total_sizes = 0

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


def find_dir(dir, path):
    """ Find directory item list for path. """
    if len(path) > 1:
        sub_paths = path[1: -1].split('/')
    else:
        sub_paths = []
    items = dir['items']
    for sub_path in sub_paths:
        for item in items:
            if 'dir' in item['type'] and sub_path in item['name']:
                items = item['items']
                continue
    return items


def dir_add_item(root, path, item):
    """ Add item to directory structure. """
    item_list = find_dir(root, path)
    item_list.append(item)


def total_dir_size(items, total):
    """ Find size of files in directory. """
    dir_size = 0
    for item in items:
        if 'dir' in item['type']:
            print(item['name'])
            dir_size += total_dir_size(item['items'], total)
        else:
            dir_size += item['size']
    print(dir_size)
    if total['limit'] == 0:
        if dir_size <= 100000:
            print(dir_size)
            total['size'] += dir_size
    else:
        limit_size = total['total_size'] - dir_size
        if limit_size <= total['limit']:
            print(f"under limit: {total['total_size']} - {dir_size} = {limit_size}")
            if limit_size > total['total_size'] - total['size']:
                total['size'] = dir_size
                print(f"best: {dir_size}")

    return dir_size


def main():
    """Main program."""
    args = get_args()
    dir_root = {'type': 'dir', 'name': "/", 'items': []}

    # Read input
    try:
        with open(args.input, 'rt') as file:
            current_path = ""
            line = file.readline().strip('\n')
            while line:
                if line[0] == '$':
                    # Command
                    line_split = line.split(" ")
                    command = line_split[1]
                    if 'cd' in command:
                        dir_name = line_split[2]
                        if '/' in line_split[2]:
                            print("Root")
                        if '..' in line_split[2]:
                            pos = current_path[0: -2].rfind('/')
                            current_path = current_path[0: pos + 1]
                            print(f"up to {current_path}")
                        else:
                            current_path += dir_name
                            if current_path[-1] != '/':
                                current_path += '/'
                            print(f"down to {current_path}")
                    elif 'ls' in command:
                        # list
                        line = file.readline().strip('\n')
                        while line and line[0] != '$':
                            line_split = line.split(" ")
                            if 'dir' in line_split[0]:
                                item = {'type': 'dir', 'name': line_split[1], 'items': []}
                                dir_add_item(dir_root, current_path, item)
                            else:
                                item = {'type': 'file', 'name': line_split[1], 'size': int(line_split[0])}
                                dir_add_item(dir_root, current_path, item)
                            line = file.readline().strip('\n')
                        continue
                    line = file.readline().strip('\n')

    except IOError:
        print("Failed reading file!")
        sys.exit()

    if args.second:
        total_size = {'size': 0, 'limit': 0, 'total_size': 0}
        total = total_dir_size(dir_root['items'], total_size)
        total_size = {'size': total, 'limit': 40000000, 'total_size': total}
        total = total_dir_size(dir_root['items'], total_size)
        print(total_size['size'])
    else:
        # Find dir sizes <= 100000
        total_size = {'size': 0, 'limit': 0, 'total_size': 0}
        total = total_dir_size(dir_root['items'], total_size)
        print(dir_root)
        print(total)
        print(total_size['size'])

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
