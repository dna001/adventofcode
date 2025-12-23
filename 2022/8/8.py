#!/usr/bin/env python3
"""
AdventOfCode day 8.
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
    tree_grid = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline().strip('\n')
            while line:
                tree_grid.append(line)
                line = file.readline().strip('\n')

    except IOError:
        print("Failed reading file!")
        sys.exit()

    if args.second:
        scenic_score = 0
        for y in range(1, len(tree_grid) - 1):
            for x in range(1, len(tree_grid[0]) - 1):
                # Calculate scenic score
                tree_height = int(tree_grid[y][x])
                print(f"tree: {x},{y},{tree_height}")
                score_left = 0
                score_right = 0
                score_up = 0
                score_down = 0
                # Score Left
                for x1 in reversed(range(0, x)):
                    #print(f"left: {x1},{y}")
                    if int(tree_grid[y][x1]) >= tree_height:
                        score_left += 1
                        break
                    score_left += 1
                # Score Right
                for x1 in range(x + 1, len(tree_grid[0])):
                    # print(f"right: {x1},{y}")
                    if int(tree_grid[y][x1]) >= tree_height:
                        score_right += 1
                        break
                    score_right += 1
                # Score Up
                for y1 in reversed(range(0, y)):
                    #print(f"up: {x},{y1}")
                    if int(tree_grid[y1][x]) >= tree_height:
                        score_up += 1
                        break
                    score_up += 1
                # Score Down
                for y1 in range(y + 1, len(tree_grid)):
                    # print(f"down: {x},{y1}")
                    if int(tree_grid[y1][x]) >= tree_height:
                        score_down += 1
                        break
                    score_down += 1
                score = score_left * score_right * score_up * score_down
                print(f"Scenic score: {score_left}*{score_right}*{score_up}*{score_down}={score}")
                if score > scenic_score:
                    scenic_score = score

        print(f"Best scenic score: {scenic_score}")
    else:
        tree_visible_count = len(tree_grid) * 2 + len(tree_grid[0]) * 2 - 4
        for y in range(1, len(tree_grid) - 1):
            for x in range(1, len(tree_grid[0]) - 1):
                visible = False
                tree_height = int(tree_grid[y][x])
                print(f"tree: {x},{y},{tree_height}")
                # Visible Left
                for x1 in range(0, x):
                    #print(f"left: {x1},{y}")
                    if int(tree_grid[y][x1]) >= tree_height:
                        visible = False
                        break
                    visible = True
                if not visible:
                    # Visible Right
                    for x1 in range(x + 1, len(tree_grid[0])):
                        #print(f"right: {x1},{y}")
                        if int(tree_grid[y][x1]) >= tree_height:
                            visible = False
                            break
                        visible = True
                if not visible:
                    # Visible Up
                    for y1 in range(0, y):
                        #print(f"up: {x},{y1}")
                        if int(tree_grid[y1][x]) >= tree_height:
                            visible = False
                            break
                        visible = True
                if not visible:
                    # Visible Down
                    for y1 in range(y + 1, len(tree_grid)):
                        #print(f"down: {x},{y1}")
                        if int(tree_grid[y1][x]) >= tree_height:
                            visible = False
                            break
                        visible = True
                if visible:
                    tree_visible_count += 1

        print(f"Visible tree count: {tree_visible_count}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
