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


def print_map(map):
    """Print map."""
    for row in map:
        row_string = ""
        for col in row:
            row_string += str(col)
        print(row_string)


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

    machine_list = []
    for i in range(0, len(lines), 4):
        machine = {'A': {'x': 0, 'y': 0}, 'B': {'x': 0, 'y': 0}, 'prize': {'x': 0, 'y': 0}}
        # Button A
        line = lines[i].strip('\n')
        coords = line.split(',')
        #print(coords[0].find('+'))

        x = coords[0][coords[0].find('+') + 1:]
        y = coords[1][coords[1].find('+') + 1:]
        machine['A']['x'] = int(x)
        machine['A']['y'] = int(y)
        # Button B
        line = lines[i + 1].strip('\n')
        coords = line.split(',')
        x = coords[0][coords[0].find('+') + 1:]
        y = coords[1][coords[1].find('+') + 1:]
        machine['B']['x'] = int(x)
        machine['B']['y'] = int(y)
        # Price
        line = lines[i + 2].strip('\n')
        coords = line.split(',')
        x = coords[0][coords[0].find('=') + 1:]
        y = coords[1][coords[1].find('=') + 1:]
        machine['prize']['x'] = int(x)
        machine['prize']['y'] = int(y)
        machine_list.append(machine)

    print(machine_list)

    machine_wins = []
    if args.second:
        for machine in machine_list:
            win_combos = []
            #machine['prize']['x'] += 10000000000000
            #machine['prize']['y'] += 10000000000000
            # Check all possible win combinations
            a = 0
            found = False
            while (1): # a <= 100
                a_tot_x = a * machine['A']['x']
                a_tot_y = a * machine['A']['y']
                if a_tot_x > machine['prize']['x'] or a_tot_y > machine['prize']['y']:
                    break
                x_remainder = (machine['prize']['x'] - a_tot_x) % machine['B']['x']
                y_remainder = (machine['prize']['y'] - a_tot_y) % machine['B']['y']
                if x_remainder != 0 or y_remainder != 0:
                    a += 1
                    continue
                b = (machine['prize']['x'] - a_tot_x) // machine['B']['x']
                tot_x = a_tot_x + b * machine['B']['x']
                tot_y = a_tot_y + b * machine['B']['y']
                if tot_x == machine['prize']['x'] and tot_y == machine['prize']['y']:
                    #if b <= 100:
                    tokens = a * 3 + b
                    win_combos.append({'A': a, 'B': b, 'tokens': tokens})
                    found = True
                    break
                a += 1
            if found:
                machine_wins.append(win_combos)
                print(f"{win_combos}, prize: {machine['prize']}")

    else:
        for machine in machine_list:
            win_combos = []
            # Check all possible win combinations (max 100 presses)
            for a in range(100):
                for b in range(100):
                    x_tot = a * machine['A']['x'] + b * machine['B']['x']
                    y_tot = a * machine['A']['y'] + b * machine['B']['y']
                    if x_tot == machine['prize']['x'] and y_tot == machine['prize']['y']:
                        tokens = a * 3 + b
                        win_combos.append({'A': a, 'B': b, 'tokens': tokens})
                    elif x_tot > machine['prize']['x'] or y_tot > machine['prize']['y']:
                        break
            if len(win_combos) > 0:
                print(f"{win_combos}, prize: {machine['prize']}")
                machine_wins.append(win_combos)

    token_sum = 0
    n_prizes = 0
    for wins in machine_wins:
        # Find fewest tokens
        min_tokens = 0
        for combo in wins:
            if min_tokens == 0 or min_tokens > combo['tokens']:
                min_tokens = combo['tokens']
        if min_tokens > 0:
            n_prizes += 1
            token_sum += min_tokens

    print(f"Wins: {n_prizes}, Tokens: {token_sum}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
